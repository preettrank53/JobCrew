from config import logger
from graph.state import JobCrewState

def generate_messages_node(state: JobCrewState) -> dict:
    logger.info("Running Messaging Generation Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("messaging")
        
    return {
        "messaging_output": "Placeholder Messaging: Tailored cover letter and cold outreach emails.",
        "execution_metadata": exec_metadata
    }
