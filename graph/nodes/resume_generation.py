from config import logger
from graph.state import JobCrewState

def generate_resume_node(state: JobCrewState) -> dict:
    logger.info("Running Resume Generation Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("resume_generation")
        
    return {
        "resume_output": "Placeholder Resume: Custom tailored points for the job description.",
        "execution_metadata": exec_metadata
    }
