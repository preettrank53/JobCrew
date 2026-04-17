from crewai import LLM

def get_llm():
    """
    Initializes and returns a new instance of the local Ollama LLM.
    """
    return LLM(
        model="ollama/phi",
        base_url="http://localhost:11434"
    )

# Module-level singleton
llm = get_llm()

if __name__ == "__main__":
    # Test block
    print("Testing local Ollama LLM connection...")
    try:
        response = llm.call(messages=[{"role": "user", "content": "Respond with one word: ready"}])
        print(f"LLM Response: {response.strip()}")
    except Exception as e:
        print(f"Error testing LLM: {e}\n\n⚠️ IMPORTANT: Make sure the Ollama app is running on your computer and you have downloaded the model by typing 'ollama run phi' in your terminal.")


