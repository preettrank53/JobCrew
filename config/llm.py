import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

PROVIDER_GROQ = "Groq (Free & Fast - Recommended)"
PROVIDER_GEMINI = "Google Gemini"
PROVIDER_OPENAI = "OpenAI"


def get_llm(api_key=None, provider=None, fast_mode=False):
    """
    Returns a CrewAI LLM instance.

    Priority:
      1. If api_key and provider are supplied (user-provided key), use them.
      2. Otherwise fall back to the server-side GROQ_API_KEY environment variable.
    """
    temperature = 0.1 if fast_mode else 0.7
    max_tokens = 800 if fast_mode else None

    if api_key and provider:
        if provider == PROVIDER_GROQ:
            kwargs = dict(
                model="groq/llama-3.3-70b-versatile",
                api_key=api_key,
                temperature=temperature,
            )
            if max_tokens:
                kwargs["max_tokens"] = max_tokens
            return LLM(**kwargs)

        elif provider == PROVIDER_GEMINI:
            return LLM(
                model="gemini/gemini-1.5-flash",
                api_key=api_key,
                temperature=temperature,
            )

        elif provider == PROVIDER_OPENAI:
            return LLM(
                model="gpt-4o-mini",
                api_key=api_key,
                temperature=temperature,
            )

    # Server-side fallback (owner key)
    kwargs = dict(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY", ""),
        temperature=temperature,
    )
    if max_tokens:
        kwargs["max_tokens"] = max_tokens
    return LLM(**kwargs)


def get_fast_llm():
    """Returns the server-side LLM in fast mode (low-latency settings)."""
    return get_llm(fast_mode=True)


def get_user_llm(fast_mode=False):
    """
    Reads the user-provided API key and provider from Streamlit session state
    and returns a configured LLM instance.

    Raises ValueError if no key has been saved.
    """
    try:
        import streamlit as st
        user_key = st.session_state.get("user_llm_key", "").strip()
        provider = st.session_state.get("llm_provider", PROVIDER_GROQ)
    except Exception:
        user_key = ""
        provider = PROVIDER_GROQ

    if not user_key:
        raise ValueError(
            "No LLM API key configured — please add your API key in the sidebar before running the pipeline."
        )

    return get_llm(api_key=user_key, provider=provider, fast_mode=fast_mode)


# Module-level singleton (server key, used only for profile extraction fallback)
llm = get_llm()


if __name__ == "__main__":
    print("Testing server-side Groq LLM connection...")
    try:
        response = llm.call(messages=[{"role": "user", "content": "Respond with one word: ready"}])
        print(f"LLM Response: {response.strip()}")
    except Exception as e:
        print(f"Error: {e}\n\nEnsure GROQ_API_KEY is set in your .env file.")
