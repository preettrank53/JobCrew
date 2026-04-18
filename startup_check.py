import os

def run_startup_checks():
    """
    Performs a lightweight validation of the environment and filesystem.
    Returns: dict with 'passed' (bool), 'warnings' (list), 'errors' (list)
    """
    results = {
        "passed": True,
        "warnings": [],
        "errors": []
    }
    
    # 1. Check required environment variables
    required_vars = ["GROQ_API_KEY", "USAJOBS_API_KEY", "USAJOBS_USER_AGENT"]
    
    # We use a helper here to check both env and st.secrets conceptually 
    # but since this script is called from within the app, 
    # we can import settings or just check os.environ (which is populated by st.secrets too)
    for var in required_vars:
        # Check os.environ first as it's populated by both .env and Streamlit secrets fallback in our case
        # Wait, st.secrets doesn't necessarily populate os.environ automatically.
        # But our config/settings.py already handles the logic. 
        # For simplicity and isolation in this check, we'll try to import and check.
        try:
            from config.settings import get_secret
            val = get_secret(var)
        except ImportError:
            val = os.getenv(var)
            
        if not val or val.strip() == "":
            results["errors"].append(f"Missing required environment variable: {var}")
            results["passed"] = False

    # 2. Check and create necessary directories
    directories = ["logs", "outputs"]
    for dir_name in directories:
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name, exist_ok=True)
            
            # Test writability
            test_file = os.path.join(dir_name, ".write_test")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            results["errors"].append(f"Directory check failed for '{dir_name}': {str(e)}")
            results["passed"] = False

    return results
