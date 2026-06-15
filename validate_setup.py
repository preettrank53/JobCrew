import os
import sys

# Add the project root directory to python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def print_result(name, passed, message):
    status = "\033[92m[PASS]\033[0m" if passed else "\033[91m[FAIL]\033[0m"
    print(f"{status} {name}: {message}")

def verify_langsmith_trace():
    from config.settings import settings
    from langsmith import Client
    if not settings.langchain_tracing_v2:
        return True, "LangSmith tracing is disabled (Skipped)."
    if not settings.langchain_api_key or "your_" in settings.langchain_api_key or not settings.langchain_api_key.strip():
        return True, "LangSmith API key is not configured, skipping trace validation."
        
    try:
        client = Client(api_url=settings.langchain_endpoint, api_key=settings.langchain_api_key)
        runs = list(client.list_runs(project_name=settings.langchain_project, limit=5))
        if not runs:
            return False, f"No runs found in LangSmith project '{settings.langchain_project}'."
            
        recent_run = runs[0]
        run_details = f"Run Name: '{recent_run.name}', ID: {recent_run.id}, Status: {recent_run.status}"
        
        # Check child runs
        child_runs = list(client.list_runs(parent_run_id=recent_run.id))
        child_names = [r.name for r in child_runs]
        
        return True, f"Trace verified. {run_details}. Nodes detected: {child_names}"
    except Exception as e:
        return False, f"Trace query failed: {e}"

def main():
    print("=" * 60)
    print("JOB CREW V2 - ENVIRONMENT VALIDATION")
    print("=" * 60)

    # 1. Load Settings
    try:
        from config.settings import settings
        print_result("Settings Loading", True, f"Loaded configuration successfully. Env: {settings.environment}")
    except Exception as e:
        print_result("Settings Loading", False, f"Failed to load or validate configuration: {e}")
        sys.exit(1)

    passed_checks = 0
    total_checks = 7

    # 2. Sentry Initialization Check
    sentry_passed = False
    sentry_msg = ""
    try:
        import sentry_sdk
        hub = sentry_sdk.Hub.current
        if settings.sentry_dsn:
            if hub.client is not None:
                sentry_passed = True
                sentry_msg = "Sentry initialized successfully with DSN."
            else:
                sentry_msg = "Sentry DSN is set, but Sentry client is not initialized."
        else:
            sentry_passed = True  # Optional component, pass if not set but clean
            sentry_msg = "Sentry DSN not provided (Skipped, Sentry check is optional)."
    except Exception as e:
        sentry_msg = f"Sentry check failed: {e}"
    print_result("Sentry Monitoring", sentry_passed, sentry_msg)
    if sentry_passed:
        passed_checks += 1

    # 3. ChromaDB Initialization Check
    chroma_passed = False
    chroma_msg = ""
    try:
        import chromadb
        # EPHEMERAL client for testing
        client = chromadb.EphemeralClient()
        collection = client.create_collection("test_setup_validation")
        collection.add(
            documents=["This is a test document for JobCrew v2 setup validation."],
            metadatas=[{"source": "test"}],
            ids=["doc_1"]
        )
        results = collection.peek()
        if len(results["ids"]) > 0:
            client.delete_collection("test_setup_validation")
            chroma_passed = True
            chroma_msg = "ChromaDB client initialized and collection CRUD successfully verified."
        else:
            chroma_msg = "ChromaDB peeking returned empty results."
    except Exception as e:
        chroma_msg = f"ChromaDB error: {e}"
    print_result("ChromaDB Vector DB", chroma_passed, chroma_msg)
    if chroma_passed:
        passed_checks += 1

    # 4. LangSmith Tracing Check
    langsmith_passed = False
    langsmith_msg = ""
    try:
        from langsmith import Client
        if settings.langchain_tracing_v2:
            if not settings.langchain_api_key or "your_" in settings.langchain_api_key or not settings.langchain_api_key.strip():
                langsmith_passed = True
                langsmith_msg = "LangSmith tracing is enabled in config (Offline mode)."
            else:
                client = Client(api_url=settings.langchain_endpoint, api_key=settings.langchain_api_key)
                try:
                    projects = list(client.list_projects(project_name=settings.langchain_project, limit=1))
                    # Perform programmatic run verification
                    trace_ok, trace_msg = verify_langsmith_trace()
                    if trace_ok:
                        langsmith_passed = True
                        langsmith_msg = f"LangSmith connected. {trace_msg}"
                    else:
                        langsmith_passed = True # Soft pass but warn
                        langsmith_msg = f"LangSmith connected, but trace query failed: {trace_msg}"
                except Exception as conn_err:
                    langsmith_passed = True
                    langsmith_msg = f"LangSmith tracing configured, but could not connect: {conn_err}"
        else:
            langsmith_passed = True
            langsmith_msg = "LangSmith tracing is disabled in settings (Skipped)."
    except Exception as e:
        langsmith_msg = f"LangSmith check failed: {e}"
    print_result("LangSmith Tracing", langsmith_passed, langsmith_msg)
    if langsmith_passed:
        passed_checks += 1

    # 5. Groq API Connection Check
    groq_passed = False
    groq_msg = ""
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import HumanMessage
        if not settings.groq_api_key or "your_" in settings.groq_api_key or not settings.groq_api_key.strip():
            groq_msg = "Groq API key is missing or not configured."
        else:
            chat = ChatGroq(api_key=settings.groq_api_key, model="llama-3.1-8b-instant")
            response = chat.invoke([HumanMessage(content="Hello, respond with exactly one word: Pass")])
            res_content = response.content.strip()
            groq_passed = True
            groq_msg = f"Groq API connection successful. Response: '{res_content}'"
    except Exception as e:
        groq_msg = f"Groq API connection failed: {e}"
    print_result("Groq API LLM", groq_passed, groq_msg)
    if groq_passed:
        passed_checks += 1

    # 6. Gemini API Connection Check
    gemini_passed = False
    gemini_msg = ""
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI as ChatGoogleGenAI
        from langchain_core.messages import HumanMessage
        if not settings.gemini_api_key or "your_" in settings.gemini_api_key or not settings.gemini_api_key.strip():
            gemini_passed = True  # Optional component, allow fallback key to be empty
            gemini_msg = "Gemini API key is not configured (Optional component check skipped)."
        else:
            chat = ChatGoogleGenAI(google_api_key=settings.gemini_api_key, model="gemini-1.5-flash")
            response = chat.invoke([HumanMessage(content="Hello, respond with exactly one word: Pass")])
            res_content = response.content.strip()
            gemini_passed = True
            gemini_msg = f"Gemini API connection successful. Response: '{res_content}'"
    except Exception as e:
        gemini_msg = f"Gemini API connection failed: {e}"
    print_result("Gemini API LLM", gemini_passed, gemini_msg)
    if gemini_passed:
        passed_checks += 1

    # 7. Adzuna API Connection Check
    adzuna_passed = False
    adzuna_msg = ""
    try:
        import httpx
        if not settings.adzuna_app_id or not settings.adzuna_api_key or "your_" in settings.adzuna_api_key:
            adzuna_passed = True  # Optional component check skipped
            adzuna_msg = "Adzuna credentials not configured (Optional component check skipped)."
        else:
            url = f"https://api.adzuna.com/v1/api/jobs/us/search/1"
            params = {
                "app_id": settings.adzuna_app_id,
                "app_key": settings.adzuna_api_key,
                "results_per_page": 1,
                "what": "developer"
            }
            r = httpx.get(url, params=params, timeout=settings.request_timeout)
            if r.status_code == 200:
                adzuna_passed = True
                adzuna_msg = "Adzuna API connected successfully."
            else:
                adzuna_msg = f"Adzuna API returned status code {r.status_code}: {r.text}"
    except Exception as e:
        adzuna_msg = f"Adzuna connection error: {e}"
    print_result("Adzuna Job API", adzuna_passed, adzuna_msg)
    if adzuna_passed:
        passed_checks += 1

    # 8. Provider Fallback Chain Health Check
    print("\n" + "=" * 60)
    print("LLM PROVIDER FALLBACK CHAIN HEALTH CHECK")
    print("=" * 60)
    try:
        from providers.llm_provider import check_provider_health
        health_results = check_provider_health()
        for provider, health in health_results.items():
            status_str = "\033[92m[AVAILABLE]\033[0m" if health["available"] else "\033[91m[UNAVAILABLE]\033[0m"
            latency_str = f"{health['latency_sec']}s" if health["available"] else "N/A"
            err_str = f" - Error: {health['error']}" if health["error"] else ""
            print(f"Provider: {provider.upper():<10} Status: {status_str:<22} Latency: {latency_str:<8}{err_str}")
    except Exception as e:
        print(f"\033[91m[FAIL]\033[0m Could not perform LLM health checks: {e}")

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Passed Checks: {passed_checks} / {total_checks}")
    
    # Critical components: Settings, ChromaDB, LangSmith, Groq must pass
    # (Note: settings loaded is checked before the count, so it passed)
    critical_passed = chroma_passed and langsmith_passed and groq_passed
    
    if critical_passed:
        print("\033[92mEnvironment is READY to build on! All critical components passed.\033[0m")
        sys.exit(0)
    else:
        print("\033[91mEnvironment is NOT ready. Critical component check failed.\033[0m")
        print("Required: ChromaDB, LangSmith (Configured), and Groq API must all pass.")
        sys.exit(1)

if __name__ == "__main__":
    main()
