import time
from typing import List, Optional, Any, Dict
import httpx

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.callbacks import CallbackManagerForLLMRun

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
# Custom ChatOllama definition since langchain-community has deprecated/removed it
class ChatOllama(BaseChatModel):
    base_url: str = "http://localhost:11434"
    model: str = "llama3"
    temperature: float = 0.3
    
    @property
    def _llm_type(self) -> str:
        return "ollama_chat"
        
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Convert messages to Ollama api format
        formatted_msgs = []
        for msg in messages:
            role = "user"
            if msg.type == "ai":
                role = "assistant"
            elif msg.type == "system":
                role = "system"
            formatted_msgs.append({"role": role, "content": msg.content})
            
        payload = {
            "model": self.model,
            "messages": formatted_msgs,
            "options": {"temperature": self.temperature},
            "stream": False
        }
        
        try:
            import requests
            url = f"{self.base_url.rstrip('/')}/api/chat"
            res = requests.post(url, json=payload, timeout=settings.request_timeout)
            res.raise_for_status()
            data = res.json()
            content = data["message"]["content"]
            
            aimsg = AIMessage(content=content)
            return ChatResult(generations=[ChatGeneration(message=aimsg)])
        except Exception as e:
            raise RuntimeError(f"Ollama local instance call failed: {e}")

from config import settings, logger

# Helper to identify infrastructure-related errors
def is_infrastructure_error(exc: Exception) -> bool:
    exc_name = type(exc).__name__
    
    # Check rate limit/quota exception names across SDKs
    infra_error_names = [
        "RateLimitError", "APIConnectionError", "APIStatusError",
        "GoogleAPICallError", "ResourceExhausted", "ServiceUnavailable",
        "ConnectError", "TimeoutException", "ConnectTimeout"
    ]
    if exc_name in infra_error_names:
        return True
        
    # Inspect HTTP status code if present
    if hasattr(exc, "status_code") and exc.status_code in [429, 503, 504, 408]:
        return True
        
    # Inspect http status via httpx errors
    if isinstance(exc, (httpx.HTTPStatusError, httpx.RequestError, httpx.TimeoutException)):
        if isinstance(exc, httpx.HTTPStatusError):
            return exc.response.status_code in [429, 503, 504, 408]
        return True
        
    # Catch string representations
    err_str = str(exc).lower()
    if "rate limit" in err_str or "quota exceeded" in err_str or "429" in err_str or "503" in err_str or "timeout" in err_str:
        return True
        
    return False

# Custom ChatModel wrapper that implements fallback execution
class FallbackChatModel(BaseChatModel):
    fallback_chain: List[Dict[str, Any]]  # List of {"name": name, "model": BaseChatModel}
    mode: str
    
    @property
    def _llm_type(self) -> str:
        return "fallback_chat_model"
        
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        errors_logged = {}
        fallback_occurred = False
        
        for idx, provider_cfg in enumerate(self.fallback_chain):
            name = provider_cfg["name"]
            model = provider_cfg["model"]
            
            logger.info("Attempting LLM invocation", provider=name, mode=self.mode, index=idx)
            start_time = time.time()
            
            try:
                # Add LangSmith metadata dynamically if run_manager is active
                if run_manager:
                    # LangGraph/LangChain run manager child execution tracing metadata
                    pass
                
                # Call underlying model
                # Pass run_manager child callbacks to ensure child spans appear in LangSmith
                callbacks = None
                if run_manager and hasattr(run_manager, "get_child"):
                    callbacks = run_manager.get_child()
                elif run_manager:
                    # Fallback if get_child is not present
                    pass
                
                response = model.generate(
                    [messages], 
                    stop=stop, 
                    callbacks=callbacks, 
                    **kwargs
                )
                
                latency = time.time() - start_time
                logger.info("LLM invocation successful", provider=name, latency_sec=round(latency, 2))
                
                # Append provider tracing metadata to Response Metadata for state integration
                if response.generations and response.generations[0]:
                    gen = response.generations[0][0]
                    if isinstance(gen.message, AIMessage):
                        gen.message.response_metadata["provider"] = name
                        gen.message.response_metadata["model"] = getattr(model, "model_name", getattr(model, "model", "unknown"))
                        gen.message.response_metadata["latency_sec"] = latency
                        gen.message.response_metadata["fallback_occurred"] = fallback_occurred
                
                # Convert LLMResult to ChatResult
                return ChatResult(generations=response.generations[0], llm_output=response.llm_output)
                
            except Exception as e:
                latency = time.time() - start_time
                if is_infrastructure_error(e):
                    logger.warning("LLM provider failed due to infrastructure error", 
                                   provider=name, 
                                   error=str(e), 
                                   latency_sec=round(latency, 2))
                    errors_logged[name] = str(e)
                    fallback_occurred = True
                    continue
                else:
                    # Re-raise standard prompt or logic errors immediately without falling back
                    logger.error("LLM provider failed due to logic/validation error", 
                                 provider=name, 
                                 error=str(e))
                    raise e
                    
        # If we reached here, all providers failed
        error_msg = "All LLM providers in fallback chain failed: " + "; ".join([f"{k}: {v}" for k, v in errors_logged.items()])
        logger.error(error_msg)
        raise RuntimeError(error_msg)

# Factory to build specific provider models
def build_provider_model(name: str, mode: str, api_key: Optional[str] = None) -> Optional[BaseChatModel]:
    name = name.lower()
    
    # Configure parameters based on mode
    temperature = 0.3 if mode == "standard" else 0.1
    max_tokens = None if mode == "standard" else 1024
    
    if name == "groq":
        key = api_key or settings.groq_api_key
        if not key or "your_" in key or not key.strip():
            return None
        model_name = "llama-3.3-70b-versatile" if mode == "standard" else "llama-3.1-8b-instant"
        return ChatGroq(api_key=key, model=model_name, temperature=temperature, max_tokens=max_tokens)
        
    elif name == "gemini":
        key = api_key or settings.gemini_api_key
        if not key or "your_" in key or not key.strip():
            return None
        # google-genai package model name
        model_name = "gemini-1.5-flash"
        return ChatGoogleGenerativeAI(google_api_key=key, model=model_name, temperature=temperature, max_output_tokens=max_tokens)
        
    elif name == "openrouter":
        key = api_key or settings.openrouter_api_key
        if not key or "your_" in key or not key.strip():
            return None
        return ChatOpenAI(
            api_key=key,
            base_url="https://openrouter.ai/api/v1",
            model=settings.openrouter_model,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
    elif name == "ollama":
        # Ollama requires no key and runs locally
        return ChatOllama(
            base_url=settings.ollama_base_url, 
            model=settings.ollama_model,
            temperature=temperature
        )
        
    return None

# User-provided Key Execution (Bypasses fallback chain)
def get_user_llm(provider_name: str, api_key: str, mode: str = "standard") -> BaseChatModel:
    model = build_provider_model(provider_name, mode, api_key=api_key)
    if not model:
        raise ValueError(f"Could not initialize provider '{provider_name}' with the provided API key.")
    return model

# Main retrieval function for standard/fast modes
def get_llm(mode: str = "standard") -> BaseChatModel:
    fallback_chain = []
    
    # Build the fallback list in priority order
    for name in ["groq", "gemini", "openrouter", "ollama"]:
        try:
            model = build_provider_model(name, mode)
            if model:
                fallback_chain.append({"name": name, "model": model})
        except Exception as e:
            logger.warning("Failed to initialize provider during boot check", provider=name, error=str(e))
            
    if not fallback_chain:
        raise RuntimeError("No LLM providers could be initialized. Please check API keys in settings.")
        
    # Return wrapped fallback model
    return FallbackChatModel(fallback_chain=fallback_chain, mode=mode)

# Health Check Utility
def check_provider_health() -> Dict[str, Dict[str, Any]]:
    health_status = {}
    test_message = [AIMessage(content="healthcheck")] # minimally structured message
    
    for name in ["groq", "gemini", "openrouter", "ollama"]:
        health_status[name] = {"available": False, "latency_sec": 0.0, "error": None}
        
        try:
            model = build_provider_model(name, mode="fast")
            if not model:
                health_status[name]["error"] = "API key not configured."
                continue
                
            start = time.time()
            # Minimal prompt test
            model.invoke("Respond with one word: OK")
            latency = time.time() - start
            
            health_status[name]["available"] = True
            health_status[name]["latency_sec"] = round(latency, 3)
            
        except Exception as e:
            health_status[name]["error"] = str(e)
            
    return health_status
