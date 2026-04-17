import os
import sys

# Add parent directory to sys path if run directly
if __name__ == "__main__":
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_google_genai import ChatGoogleGenerativeAI
from config.settings import GEMINI_API_KEY

def get_llm():
    """
    Initializes and returns a new instance of the Google Gemini LLM.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.3,
        google_api_key=GEMINI_API_KEY
    )

# Module-level singleton
llm = get_llm()

if __name__ == "__main__":
    # Test block
    print("Testing LLM connection...")
    try:
        response = llm.invoke("Respond with one word: ready")
        print(f"LLM Response: {response.content.strip()}")
    except Exception as e:
        print(f"Error testing LLM: {e}")
