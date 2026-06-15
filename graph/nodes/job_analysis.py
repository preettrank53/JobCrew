from config import logger
from graph.state import JobCrewState
from langchain_core.messages import HumanMessage, SystemMessage

def analyze_job_node(state: JobCrewState, llm=None) -> dict:
    logger.info("Running Job Analysis Node", job_description_length=len(state.get("job_description", "")))
    
    job_description = state.get("job_description", "")
    exec_metadata = state.get("execution_metadata")
    
    if exec_metadata:
        exec_metadata.nodes_executed.append("job_analysis")
        
    if not llm:
        raise ValueError("LLM provider must be passed to the job analysis node.")
        
    # Simple version of the Job Analyzer prompt from v1
    system_prompt = (
        "You are an expert Job Analyzer. Your task is to analyze the job description and extract key "
        "requirements including required experience, primary technical skills, soft skills, educational requirements, "
        "and overall responsibilities. Format your analysis cleanly with headers."
    )
    user_prompt = f"Please analyze the following job description:\n\n{job_description}"
    
    # Call the LLM
    logger.info("Invoking LLM for job analysis")
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ])
    
    # Update execution metadata with actual provider used if available
    provider = response.response_metadata.get("provider", "unknown")
    if exec_metadata and provider != "unknown":
        exec_metadata.provider_used = provider
        
    return {
        "job_analysis": response.content,
        "execution_metadata": exec_metadata
    }
