import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_secret(key, default=""):
    """
    Retrieves a secret with the following priority:
    1. Streamlit Secrets (if running in Streamlit)
    2. Environment Variables (including those from .env)
    """
    try:
        import streamlit as st
        # Check if key exists in st.secrets
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # Fallback if Streamlit is not available or secrets not configured
        pass
    
    return os.getenv(key, default).strip()

# Constants
GROQ_API_KEY = get_secret("GROQ_API_KEY")
USAJOBS_API_KEY = get_secret("USAJOBS_API_KEY")
USAJOBS_USER_AGENT = get_secret("USAJOBS_USER_AGENT")

# Pipeline configuration
PIPELINE_MODE = get_secret("PIPELINE_MODE", "standard")
MAX_AGENT_ITERATIONS = int(get_secret("MAX_AGENT_ITERATIONS", "3"))
MAX_AGENT_RPM = int(get_secret("MAX_AGENT_RPM", "10"))
PIPELINE_TIMEOUT_SECONDS = int(get_secret("PIPELINE_TIMEOUT_SECONDS", "180"))
GROQ_TEMPERATURE = float(get_secret("GROQ_TEMPERATURE", "0.3"))

# Validation is handled by startup_check.py in app.py main()
