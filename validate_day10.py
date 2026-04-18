import os
import sys
import importlib

def print_result(check_name, passed, message=""):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {check_name}: {message}")
    if not passed:
        return False
    return True

def validate():
    print("--- JobCrew Pre-Deployment Validation ---\n")
    overall_passed = True
    failed_checks = []

    # Check 1: Deployment files present
    files_to_check = [
        ".streamlit/config.toml",
        ".streamlit/secrets.toml.example",
        "packages.txt",
        ".python-version",
        "README.md",
        "LICENSE",
        "requirements.txt",
        "requirements-dev.txt"
    ]
    total_files = len(files_to_check)
    found_files = 0
    for f in files_to_check:
        if os.path.exists(f):
            found_files += 1
        else:
            print(f"  Missing: {f}")
    
    res = print_result("File Existence", found_files == total_files, f"Found {found_files}/{total_files} files")
    if not res: failed_checks.append("File Existence"); overall_passed = False

    # Check 2: requirements.txt pinned
    pinned_count = 0
    all_pinned = True
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "==" not in line and not line.startswith("-r"):
                    all_pinned = False
                    print(f"  Unpinned package: {line}")
                else:
                    pinned_count += 1
    res = print_result("Requirement Pinning", all_pinned, f"Verified {pinned_count} pinned packages")
    if not res: failed_checks.append("Requirement Pinning"); overall_passed = False

    # Check 3: Streamlit config valid TOML
    config_valid = False
    try:
        import tomli as toml
        with open(".streamlit/config.toml", "rb") as f:
            config = toml.load(f)
            if all(k in config for k in ["theme", "server", "browser"]):
                config_valid = True
    except Exception as e:
        print(f"  TOML Error: {e}")
    res = print_result("Streamlit Config", config_valid, "Valid TOML with required sections")
    if not res: failed_checks.append("Streamlit Config"); overall_passed = False

    # Check 4: Settings loads from environment
    os.environ["GROQ_API_KEY"] = "test_groq"
    os.environ["USAJOBS_API_KEY"] = "test_usajobs"
    os.environ["USAJOBS_USER_AGENT"] = "test_agent"
    try:
        from config import settings
        importlib.reload(settings)
        settings_valid = all([
            settings.GROQ_API_KEY == "test_groq",
            settings.USAJOBS_API_KEY == "test_usajobs",
            settings.USAJOBS_USER_AGENT == "test_agent"
        ])
    except Exception as e:
        settings_valid = False
        print(f"  Settings Error: {e}")
    res = print_result("Environment Settings", settings_valid, "Settings correctly populated from environment")
    if not res: failed_checks.append("Environment Settings"); overall_passed = False

    # Check 5: Startup check passes
    try:
        from startup_check import run_startup_checks
        startup_res = run_startup_checks()
        startup_passed = startup_res["passed"] and not startup_res["errors"]
    except Exception as e:
        startup_passed = False
        print(f"  Startup check crashed: {e}")
    res = print_result("Startup Checks", startup_passed, "Environment and directory validation passed")
    if not res: failed_checks.append("Startup Checks"); overall_passed = False

    # Check 6: Git readiness
    git_ready = True
    if not os.path.exists(".git"):
        git_ready = False
        print("  .git directory missing")
    
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            content = f.read()
            for entry in [".env", "secrets.toml", "__pycache__", ".venv"]:
                if entry not in content:
                    git_ready = False
                    print(f"  .gitignore missing entry: {entry}")
    
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            if "jobcrew.streamlit.app" not in f.read():
                git_ready = False
                print("  README.md missing live demo URL")
                
    res = print_result("Git Readiness", git_ready, "Git initialized and critical ignores set")
    if not res: failed_checks.append("Git Readiness"); overall_passed = False

    # Check 7: Full app import chain
    import_passed = True
    import_list = [
        ("config.settings", "GROQ_API_KEY"),
        ("config.llm", "llm"),
        ("tools.usajobs_tool", "fetch_jobs"),
        ("tools.resume_parser", "parse_resume_file"),
        ("agents.job_analyzer", "create_job_analyzer_agent"),
        ("crew", "run_jobcrew_pipeline"),
        ("tracker", "get_all_applications")
    ]
    
    for mod_name, attr in import_list:
        try:
            mod = importlib.import_module(mod_name)
            if not hasattr(mod, attr):
                import_passed = False
                print(f"  Import Failed: Attribute '{attr}' missing in '{mod_name}'")
        except Exception as e:
            import_passed = False
            print(f"  Import Failed: {mod_name} -> {e}")
            
    res = print_result("Import Chain", import_passed, "All critical modules and functions importable")
    if not res: failed_checks.append("Import Chain"); overall_passed = False

    print("\n-------------------------------------------")
    if overall_passed:
        # Using ASCII for deployment readiness message to avoid encoding errors on Windows
        print("PASSED: JobCrew is DEPLOYMENT READY - proceed to Day 11")
    else:
        print(f"FAILED: {len(failed_checks)} checks failed - resolve before deploying")
        for f in failed_checks:
            print(f"  - {f}")

if __name__ == "__main__":
    validate()
