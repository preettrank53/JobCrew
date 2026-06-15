import datetime
from config import logger
from graph.state import JobCrewState, ExecutionMetadata

def validate_input_node(state: JobCrewState, llm=None) -> dict:
    logger.info("Running Input Validation Node", candidate_name=state.get("candidate_profile", {}).get("name", "Unknown"))
    
    # Initialize execution metadata
    now_str = datetime.datetime.utcnow().isoformat()
    errors = {}
    
    # Check minimum required fields
    candidate_profile = state.get("candidate_profile")
    job_description = state.get("job_description")
    
    if not candidate_profile or not isinstance(candidate_profile, dict):
        errors["input_validation"] = "Invalid or missing candidate_profile."
    elif not candidate_profile.get("name"):
        errors["input_validation"] = "candidate_profile is missing 'name'."
            
    if not job_description or not isinstance(job_description, str) or len(job_description.strip()) < 10:
        errors["input_validation"] = (errors.get("input_validation", "") + " Invalid or missing job_description.").strip()
        
    errors_dict = {}
    if errors:
        errors_dict = {"input_validation": errors.get("input_validation")}
        status = "failed"
    else:
        status = "validated"
        
    # Detect country
    job_country = state.get("job_country") or "unknown"
    if job_country == "unknown" and job_description:
        desc_lower = job_description.lower()
        if "united states" in desc_lower or "usa" in desc_lower or "us citizens" in desc_lower:
            job_country = "US"
        elif "united kingdom" in desc_lower or " uk " in desc_lower or "london" in desc_lower:
            job_country = "UK"
        elif "canada" in desc_lower or "ca " in desc_lower or "toronto" in desc_lower:
            job_country = "CA"
        else:
            job_country = "US" # default fallback
            
    # Detect language using a simple heuristic or short LLM call
    language = "English"
    provider_name = "System"
    
    if not errors and llm and job_description:
        try:
            from langchain_core.messages import HumanMessage
            prompt = f"Identify the language of the following job description. Respond with only the language name (e.g. English, French, Spanish, German, etc.).\n\nJob Description:\n{job_description[:500]}"
            response = llm.invoke([HumanMessage(content=prompt)])
            detected_lang = response.content.strip()
            
            # Simple sanitization
            for lang in ["English", "Spanish", "French", "German"]:
                if lang.lower() in detected_lang.lower():
                    language = lang
                    break
            
            provider_name = response.response_metadata.get("provider", "Groq")
        except Exception as e:
            logger.warning("LLM language detection failed, falling back to heuristic", error=str(e))
            language = "English"
            
    exec_metadata = ExecutionMetadata(
        start_time=now_str,
        nodes_executed=["input_validation"],
        provider_used=provider_name,
        errors=errors_dict
    )
    
    # Store language back in candidate_profile if we want, or just log it
    logger.info("Input validation result", status=status, country=job_country, language=language)
    
    return {
        "status": status,
        "job_country": job_country,
        "execution_metadata": exec_metadata
    }
