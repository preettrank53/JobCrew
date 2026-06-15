import unittest
from unittest.mock import patch
from typing import List, Optional, Any

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.outputs import ChatResult, ChatGeneration
from langchain_core.messages import AIMessage, BaseMessage

# Import code to test
from providers.llm_provider import (
    get_llm,
    get_user_llm,
    build_provider_model,
    FallbackChatModel,
)

# Custom MockChatModel to simulate successes and rate-limit errors
class MockChatModel(BaseChatModel):
    model_name: str
    should_fail: bool = False
    fail_with_infra_error: bool = True
    temperature: float = 0.3
    max_tokens: Optional[int] = None
    
    @property
    def _llm_type(self) -> str:
        return "mock_chat_model"
        
    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[Any] = None,
        **kwargs: Any,
    ) -> ChatResult:
        if self.should_fail:
            if self.fail_with_infra_error:
                raise RuntimeError("RateLimitError: 429 Too Many Requests")
            else:
                raise ValueError("Prompt logic validation error")
                
        # Return a successful response
        msg = AIMessage(
            content=f"Response from {self.model_name}", 
            response_metadata={}
        )
        gen = ChatGeneration(message=msg)
        return ChatResult(generations=[gen])

class TestProviderChain(unittest.TestCase):
    
    @patch("providers.llm_provider.build_provider_model")
    def test_primary_provider_success(self, mock_build):
        # Setup mocks
        mock_groq = MockChatModel(model_name="groq")
        mock_gemini = MockChatModel(model_name="gemini")
        
        # mock build_provider_model to return groq first, then gemini
        mock_build.side_effect = lambda name, mode, api_key=None: {
            "groq": mock_groq,
            "gemini": mock_gemini
        }.get(name)
        
        llm = get_llm("standard")
        self.assertIsInstance(llm, FallbackChatModel)
        
        # Invoke and check output
        response = llm.invoke("Test prompt")
        self.assertEqual(response.content, "Response from groq")
        self.assertEqual(response.response_metadata["provider"], "groq")
        self.assertFalse(response.response_metadata["fallback_occurred"])

    @patch("providers.llm_provider.build_provider_model")
    def test_fallback_to_second_provider(self, mock_build):
        # Setup mocks: groq rate limits, gemini succeeds
        mock_groq = MockChatModel(model_name="groq", should_fail=True)
        mock_gemini = MockChatModel(model_name="gemini")
        
        mock_build.side_effect = lambda name, mode, api_key=None: {
            "groq": mock_groq,
            "gemini": mock_gemini
        }.get(name)
        
        llm = get_llm("standard")
        
        response = llm.invoke("Test prompt")
        self.assertEqual(response.content, "Response from gemini")
        self.assertEqual(response.response_metadata["provider"], "gemini")
        self.assertTrue(response.response_metadata["fallback_occurred"])

    @patch("providers.llm_provider.build_provider_model")
    def test_all_providers_fail(self, mock_build):
        # Setup mocks: all configured models rate limit
        mock_groq = MockChatModel(model_name="groq", should_fail=True)
        mock_gemini = MockChatModel(model_name="gemini", should_fail=True)
        
        mock_build.side_effect = lambda name, mode, api_key=None: {
            "groq": mock_groq,
            "gemini": mock_gemini
        }.get(name)
        
        llm = get_llm("standard")
        
        # Should raise RuntimeError detailing all failures
        with self.assertRaises(RuntimeError) as context:
            llm.invoke("Test prompt")
            
        self.assertIn("All LLM providers in fallback chain failed", str(context.exception))
        self.assertIn("groq:", str(context.exception))
        self.assertIn("gemini:", str(context.exception))

    @patch("providers.llm_provider.build_provider_model")
    def test_no_fallback_on_logic_errors(self, mock_build):
        # Setup mocks: groq fails with a logic error (ValueError), should NOT fall back to gemini
        mock_groq = MockChatModel(model_name="groq", should_fail=True, fail_with_infra_error=False)
        mock_gemini = MockChatModel(model_name="gemini")
        
        mock_build.side_effect = lambda name, mode, api_key=None: {
            "groq": mock_groq,
            "gemini": mock_gemini
        }.get(name)
        
        llm = get_llm("standard")
        
        # ValueError should propagate directly
        with self.assertRaises(ValueError) as context:
            llm.invoke("Test prompt")
        self.assertEqual(str(context.exception), "Prompt logic validation error")

    def test_mode_parameter_resolution(self):
        # Check standard mode params
        groq_std = build_provider_model("groq", mode="standard", api_key="dummy_key")
        self.assertIsNotNone(groq_std)
        self.assertEqual(groq_std.temperature, 0.3)
        self.assertIsNone(groq_std.max_tokens)
        
        # Check fast mode params
        groq_fast = build_provider_model("groq", mode="fast", api_key="dummy_key")
        self.assertIsNotNone(groq_fast)
        self.assertEqual(groq_fast.temperature, 0.1)
        self.assertEqual(groq_fast.max_tokens, 1024)

    @patch("providers.llm_provider.build_provider_model")
    def test_user_provided_key_no_fallback(self, mock_build):
        # Setup mock: user model fails, get_user_llm must raise immediately and not look for fallbacks
        mock_user_model = MockChatModel(model_name="user_groq", should_fail=True)
        mock_build.side_effect = lambda name, mode, api_key=None: (
            mock_user_model if api_key == "user_supplied_key" else None
        )
        
        user_llm = get_user_llm("groq", "user_supplied_key", "standard")
        self.assertEqual(user_llm.model_name, "user_groq")
        
        with self.assertRaises(RuntimeError):
            user_llm.invoke("Test")

if __name__ == '__main__':
    unittest.main()
