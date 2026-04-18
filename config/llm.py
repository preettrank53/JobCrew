import os
from crewai import LLM
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    """
    Initializes and returns a new instance of the Groq API LLM.
    """
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY", "your-key-here")
    )

def get_fast_llm():
    """
    Returns a fast LLM instance with lower temperature and reduced token limit.
    Optimized for speed over detail.
    """
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY", "your-key-here"),
        temperature=0.1,
        max_tokens=800
    )

# Module-level singleton
llm = get_llm()

if __name__ == "__main__":
    # Test block
    print("Testing Groq LLM connection...")
    try:
        response = llm.call(messages=[{"role": "user", "content": "Respond with one word: ready"}])
        print(f"LLM Response: {response.strip()}")
    except Exception as e:
        print(f"Error testing LLM: {e}\n\n⚠️ IMPORTANT: Ensure your GROQ_API_KEY is correctly added to your .env file.")
