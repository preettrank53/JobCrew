import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
USAJOBS_API_KEY = os.getenv("USAJOBS_API_KEY", "").strip()
USAJOBS_USER_AGENT = os.getenv("USAJOBS_USER_AGENT", "").strip()

# Pipeline configuration
PIPELINE_MODE = os.getenv("PIPELINE_MODE", "standard").strip()
MAX_AGENT_ITERATIONS = int(os.getenv("MAX_AGENT_ITERATIONS", "3"))
MAX_AGENT_RPM = int(os.getenv("MAX_AGENT_RPM", "10"))
PIPELINE_TIMEOUT_SECONDS = int(os.getenv("PIPELINE_TIMEOUT_SECONDS", "180"))
GROQ_TEMPERATURE = float(os.getenv("GROQ_TEMPERATURE", "0.3"))

if not USAJOBS_API_KEY:
    raise EnvironmentError("USAJOBS_API_KEY is not set in the environment. Please check your .env file.")

