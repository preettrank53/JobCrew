import datetime
from config import logger
from graph.state import JobCrewState

def finalize_output_node(state: JobCrewState) -> dict:
    logger.info("Running Output Finalization Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("output_finalization")
        exec_metadata.end_time = datetime.datetime.utcnow().isoformat()
        
    status = "failed" if state.get("status") == "failed" else "completed"
    return {
        "status": status,
        "execution_metadata": exec_metadata
    }
