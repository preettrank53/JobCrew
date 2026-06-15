from config import logger
from graph.state import JobCrewState

def prep_interview_node(state: JobCrewState) -> dict:
    logger.info("Running Interview Prep Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("interview_prep")
        
    return {
        "interview_prep_output": "Placeholder Interview Prep: 10 customized STAR questions and frameworks.",
        "execution_metadata": exec_metadata
    }
