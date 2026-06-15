from config import logger
from graph.state import JobCrewState, QualityScore

def evaluate_quality_node(state: JobCrewState) -> dict:
    logger.info("Running Quality Evaluation Node")
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("quality_evaluation")
        
    # Standard dummy quality scores
    scores = {
        "job_analysis": QualityScore(agent_name="Job Analyzer", score=9.0, passed=True, feedback="Great analysis"),
        "resume": QualityScore(agent_name="Resume Agent", score=8.5, passed=True, feedback="Good tailoring"),
    }
    
    return {
        "quality_scores": scores,
        "execution_metadata": exec_metadata
    }
