from config import logger
from graph.state import JobCrewState, FitScore

def score_fit_node(state: JobCrewState) -> dict:
    candidate = state.get("candidate_profile", {})
    # Support overriding fit score in tests to test different routing paths
    test_score = float(candidate.get("test_fit_score", 8.5))
    
    logger.info("Running Fit Scoring Node", assigned_score=test_score)
    
    fit_score_obj = FitScore(
        overall_score=test_score,
        dimension_breakdown={
            "experience": test_score - 0.5,
            "skills": test_score + 0.2,
            "education": test_score
        },
        summary=f"Placeholder fit scoring summary with an overall score of {test_score}."
    )
    
    exec_metadata = state.get("execution_metadata")
    if exec_metadata:
        exec_metadata.nodes_executed.append("fit_scoring")
        
    return {
        "fit_score": fit_score_obj,
        "execution_metadata": exec_metadata
    }
