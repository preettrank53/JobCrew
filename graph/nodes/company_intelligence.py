from config import logger
from graph.state import JobCrewState

def fetch_company_intel_node(state: JobCrewState) -> dict:
    logger.info("Running Company Intelligence Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("company_intelligence")
        
    return {
        "company_intel_output": "Placeholder Company Intel: Key facts, tech stack, culture notes.",
        "execution_metadata": exec_metadata
    }
