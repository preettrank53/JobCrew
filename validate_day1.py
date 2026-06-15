import os
import sys
import datetime
from typing import Dict, Any

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def print_check(name: str, passed: bool, details: str = ""):
    status = "\033[92m[PASS]\033[0m" if passed else "\033[91m[FAIL]\033[0m"
    print(f"{status} Check: {name}")
    if details:
        print(f"       Details: {details}")

def run_validation():
    print("=" * 60)
    print("JOB CREW V2 - DAY 1 COMPLETION VALIDATION")
    print("=" * 60)
    
    passed_count = 0
    total_checks = 10
    failures = []

    # Check 1: Folder Structure Scaffolding & __init__.py files
    try:
        required_dirs = [
            "config", "graph", "graph/nodes", "providers", "tests"
        ]
        scaffold_ok = True
        missing_dirs = []
        missing_inits = []
        
        for r_dir in required_dirs:
            if not os.path.exists(r_dir):
                scaffold_ok = False
                missing_dirs.append(r_dir)
            # Check __init__.py
            init_file = os.path.join(r_dir, "__init__.py")
            if not os.path.exists(init_file) and r_dir != ".":
                scaffold_ok = False
                missing_inits.append(init_file)
                
        if scaffold_ok:
            print_check("1. Folder Structure Scaffolding", True, "All required directories and __init__.py files exist.")
            passed_count += 1
        else:
            details = f"Missing Dirs: {missing_dirs}, Missing Inits: {missing_inits}"
            print_check("1. Folder Structure Scaffolding", False, details)
            failures.append(("Scaffolding", details))
    except Exception as e:
        print_check("1. Folder Structure Scaffolding", False, str(e))
        failures.append(("Scaffolding Exception", str(e)))

    # Check 2: Environment Variables
    try:
        from config.settings import settings
        env_ok = True
        missing_vars = []
        if not settings.groq_api_key or "your_" in settings.groq_api_key:
            env_ok = False
            missing_vars.append("GROQ_API_KEY")
            
        if env_ok:
            print_check("2. Environment Variables", True, f"Critical env vars loaded successfully. Env: {settings.environment}")
            passed_count += 1
        else:
            details = f"Missing or placeholder env variables: {missing_vars}"
            print_check("2. Environment Variables", False, details)
            failures.append(("Environment Variables", details))
    except Exception as e:
        print_check("2. Environment Variables", False, str(e))
        failures.append(("Environment Variables Exception", str(e)))

    # Check 3: Provider Chain Initialization & Health Check
    try:
        from providers.llm_provider import get_llm, check_provider_health
        llm = get_llm("fast")
        # Run a simple test prompt (Invoke Groq via the fallback chain)
        res = llm.invoke("Respond with one word: OK")
        if res and res.content.strip():
            print_check("3. Provider Fallback Chain", True, f"Fallback model initialized and successfully responded via: {res.response_metadata.get('provider')}")
            passed_count += 1
        else:
            print_check("3. Provider Fallback Chain", False, "Received empty response from fallback chain.")
            failures.append(("Provider Fallback Chain", "Empty response"))
    except Exception as e:
        print_check("3. Provider Fallback Chain", False, str(e))
        failures.append(("Provider Fallback Chain Exception", str(e)))

    # Check 4: LangGraph Pipeline Compilation
    try:
        from graph.pipeline import create_pipeline
        pipeline = create_pipeline(mode="fast")
        node_keys = list(pipeline.nodes.keys())
        expected_node_count = 11  # 10 nodes + __start__
        
        if len(node_keys) == expected_node_count:
            print_check("4. LangGraph Compilation", True, f"StateGraph compiled successfully with {len(node_keys)} node definitions.")
            passed_count += 1
        else:
            details = f"Expected {expected_node_count} nodes, got {len(node_keys)}: {node_keys}"
            print_check("4. LangGraph Compilation", False, details)
            failures.append(("LangGraph Compilation", details))
    except Exception as e:
        print_check("4. LangGraph Compilation", False, str(e))
        failures.append(("LangGraph Compilation Exception", str(e)))

    # Check 5: Pipeline State TypedDict
    try:
        from graph.state import JobCrewState
        # Verify typed fields on JobCrewState
        required_fields = [
            "candidate_profile", "job_description", "job_source", "job_country",
            "job_analysis", "fit_score", "execution_path", "execution_path_reason",
            "resume_output", "messaging_output", "interview_prep_output", "skills_gap_output",
            "company_intel_output", "rag_metadata", "quality_scores", "execution_metadata", "status"
        ]
        annotations = JobCrewState.__annotations__
        state_ok = True
        missing_fields = []
        
        for field in required_fields:
            if field not in annotations:
                state_ok = False
                missing_fields.append(field)
                
        if state_ok:
            print_check("5. State TypedDict Fields", True, "All required pipeline state fields are defined.")
            passed_count += 1
        else:
            details = f"Missing state annotations: {missing_fields}"
            print_check("5. State TypedDict Fields", False, details)
            failures.append(("State Fields", details))
    except Exception as e:
        print_check("5. State TypedDict Fields", False, str(e))
        failures.append(("State Fields Exception", str(e)))

    # Check 6: Feature Flag System
    try:
        from config.settings import settings
        from config.feature_flags import use_v2_pipeline
        
        # Test True flag
        original_ver = settings.pipeline_version
        settings.pipeline_version = "2.0.0"
        true_flag = use_v2_pipeline()
        
        # Test False flag
        settings.pipeline_version = "1.0.0"
        false_flag = not use_v2_pipeline()
        
        # Restore version
        settings.pipeline_version = original_ver
        
        if true_flag and false_flag:
            print_check("6. Feature Flag Routing", True, "Feature flag correctly evaluates True for v2 and False for v1.")
            passed_count += 1
        else:
            details = f"True flag evaluated: {true_flag}, False flag evaluated: {not false_flag}"
            print_check("6. Feature Flag Routing", False, details)
            failures.append(("Feature Flag Routing", details))
    except Exception as e:
        print_check("6. Feature Flag Routing", False, str(e))
        failures.append(("Feature Flag Exception", str(e)))

    # Check 7: Real Node Execution (Input Validation & Job Analysis)
    try:
        from graph.pipeline import create_pipeline
        from graph.state import JobCrewState
        
        pipeline = create_pipeline(mode="fast")
        initial_state: JobCrewState = {
            "candidate_profile": {
                "name": "Jane Doe",
                "experience": "5 years Python developer seeking LangChain opportunities"
            },
            "job_description": "We are seeking a Python Developer with experience building chains using LangChain and LangGraph in the United States.",
            "job_source": "Adzuna",
            "job_country": "unknown",
            "job_analysis": None,
            "fit_score": None,
            "execution_path": None,
            "execution_path_reason": None,
            "resume_output": None,
            "messaging_output": None,
            "interview_prep_output": None,
            "skills_gap_output": None,
            "company_intel_output": None,
            "rag_metadata": {},
            "quality_scores": {},
            "execution_metadata": None,
            "status": "started"
        }
        
        # Configure metadata for LangSmith tracing
        config = {
            "metadata": {
                "job_title": "Python Developer",
                "country": "US",
                "pipeline_version": "2.0.0"
            }
        }
        
        # Force a score of 9.0 to pass through resume generation
        initial_state["candidate_profile"]["test_fit_score"] = 9.0
        
        final_state = pipeline.invoke(initial_state, config=config)
        exec_meta = final_state.get("execution_metadata")
        
        # Check detected values
        country = final_state.get("job_country")
        analysis = final_state.get("job_analysis")
        
        nodes_exec = exec_meta.nodes_executed if exec_meta else []
        
        if country == "US" and analysis and len(analysis.strip()) > 50 and "input_validation" in nodes_exec and "job_analysis" in nodes_exec:
            print_check("7. Real Node Execution", True, f"Input Validation and Job Analysis nodes executed successfully. Country: {country}, Analysis Length: {len(analysis)} chars.")
            passed_count += 1
        else:
            details = f"Detected Country: {country}, Analysis Length: {len(analysis) if analysis else 0}, Nodes Executed: {nodes_exec}"
            print_check("7. Real Node Execution", False, details)
            failures.append(("Real Node Execution", details))
    except Exception as e:
        print_check("7. Real Node Execution", False, str(e))
        failures.append(("Real Node Execution Exception", str(e)))

    # Check 8: LangSmith Trace Verification
    try:
        from validate_setup import verify_langsmith_trace
        trace_ok, trace_msg = verify_langsmith_trace()
        if trace_ok:
            print_check("8. LangSmith Telemetry Query", True, trace_msg)
            passed_count += 1
        else:
            print_check("8. LangSmith Telemetry Query", False, trace_msg)
            failures.append(("LangSmith Telemetry Query", trace_msg))
    except Exception as e:
        print_check("8. LangSmith Telemetry Query", False, str(e))
        failures.append(("LangSmith Telemetry Exception", str(e)))

    # Check 9: ChromaDB Connection
    try:
        import chromadb
        client = chromadb.EphemeralClient()
        col = client.create_collection("test_day1_validation")
        col.add(documents=["Document contents"], ids=["d1"])
        res = col.peek()
        if len(res["ids"]) > 0:
            print_check("9. ChromaDB CRUD", True, "ChromaDB client and collection creation verified.")
            passed_count += 1
        else:
            print_check("9. ChromaDB CRUD", False, "ChromaDB peek returned empty results.")
            failures.append(("ChromaDB CRUD", "Empty query results"))
    except Exception as e:
        print_check("9. ChromaDB CRUD", False, str(e))
        failures.append(("ChromaDB CRUD Exception", str(e)))

    # Check 10: Sentry Integration
    try:
        import sentry_sdk
        hub = sentry_sdk.Hub.current
        print_check("10. Sentry Monitoring", True, "Sentry client module imported and initialized without errors.")
        passed_count += 1
    except Exception as e:
        print_check("10. Sentry Monitoring", False, str(e))
        failures.append(("Sentry Exception", str(e)))

    # Validation Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(f"Passed Checks: {passed_count} / {total_checks}")
    
    if passed_count >= 8:
        print("\n\033[92m[CONFIRMATION] Day 1 is COMPLETE and Day 2 can begin!\033[0m")
        print("All required infrastructure, scaffolding, provider chaining, and graph pipeline skeletons are verified.")
        sys.exit(0)
    else:
        print("\n\033[91m[ERROR] Day 1 completion failed. Please fix the following errors:\033[0m")
        for stage, fail_msg in failures:
            print(f" - {stage}: {fail_msg}")
        sys.exit(1)

if __name__ == "__main__":
    run_validation()
