import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "").strip()
USAJOBS_USER_AGENT = os.getenv("USAJOBS_USER_AGENT", "").strip()

if not GEMINI_API_KEY:
    raise EnvironmentError("GEMINI_API_KEY is not set in the environment. Please check your .env file.")
