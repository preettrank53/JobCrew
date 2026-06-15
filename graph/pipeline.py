import os
import sys
from typing import Dict, Any
from functools import partial

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from langgraph.graph import StateGraph, START, END
from config import settings, logger
from graph.state import JobCrewState
from providers.llm_provider import get_llm
from graph.nodes import (
    validate_input_node,
    analyze_job_node,
    score_fit_node,
    generate_resume_node,
    generate_messages_node,
    prep_interview_node,
    analyze_skills_gap_node,
    fetch_company_intel_node,
    evaluate_quality_node,
    finalize_output_node,
)

# 1. Define the conditional routing functions
def route_input_validation(state: JobCrewState) -> str:
    status = state.get("status")
    if status == "failed":
        logger.warning("Input validation failed, routing to early exit (failed).")
        return "failed"
    return "passed"

def route_fit_score(state: JobCrewState) -> str:
    fit_score = state.get("fit_score")
    if not fit_score:
        logger.warning("Fit score missing in state, defaulting to 'standard' path.")
        return "standard"
        
    overall = fit_score.overall_score
    fast_track_threshold = settings.fit_score_fast_track_threshold
    standard_threshold = settings.fit_score_standard_threshold
    
    logger.info("Routing decision point", 
                score=overall, 
                fast_track_threshold=fast_track_threshold, 
                standard_threshold=standard_threshold)
                
    if overall >= fast_track_threshold:
        state["execution_path"] = "fast_track"
        state["execution_path_reason"] = f"Fit score {overall} >= fast-track threshold {fast_track_threshold}."
        return "fast_track"
    elif overall >= standard_threshold:
        state["execution_path"] = "standard"
        state["execution_path_reason"] = f"Fit score {overall} is between {standard_threshold} and {fast_track_threshold}."
        return "standard"
    else:
        state["execution_path"] = "gap_focus"
        state["execution_path_reason"] = f"Fit score {overall} < standard threshold {standard_threshold}."
        return "gap_focus"

# 2. Assemble and Compile StateGraph dynamically based on mode
def create_pipeline(mode: str = "standard"):
    logger.info("Assembling StateGraph pipeline", mode=mode)
    
    # Initialize the LLM provider chain with the specific mode
    llm = get_llm(mode=mode)
    
    workflow = StateGraph(JobCrewState)
    
    # Add all nodes, wrapping LLM-dependent nodes with partial binding
    workflow.add_node("input_validation", partial(validate_input_node, llm=llm))
    workflow.add_node("job_analysis", partial(analyze_job_node, llm=llm))
    workflow.add_node("fit_scoring", score_fit_node)
    workflow.add_node("resume_generation", generate_resume_node)
    workflow.add_node("messaging", generate_messages_node)
    workflow.add_node("interview_prep", prep_interview_node)
    workflow.add_node("skills_gap", analyze_skills_gap_node)
    workflow.add_node("company_intelligence", fetch_company_intel_node)
    workflow.add_node("quality_evaluation", evaluate_quality_node)
    workflow.add_node("output_finalization", finalize_output_node)
    
    # Entry Point & Conditional Input Validation Edge
    workflow.add_edge(START, "input_validation")
    workflow.add_conditional_edges(
        "input_validation",
        route_input_validation,
        {
            "passed": "job_analysis",
            "failed": "output_finalization"
        }
    )
    
    # Job analysis to fit scoring
    workflow.add_edge("job_analysis", "fit_scoring")
    
    # Add conditional routing edge from fit scoring
    workflow.add_conditional_edges(
        "fit_scoring",
        route_fit_score,
        {
            "fast_track": "resume_generation",
            "standard": "company_intelligence",
            "gap_focus": "skills_gap"
        }
    )
    
    # Connect branches back to finalization
    workflow.add_edge("company_intelligence", "resume_generation")
    workflow.add_edge("resume_generation", "messaging")
    workflow.add_edge("messaging", "interview_prep")
    workflow.add_edge("interview_prep", "quality_evaluation")
    
    workflow.add_edge("skills_gap", "quality_evaluation")
    
    workflow.add_edge("quality_evaluation", "output_finalization")
    workflow.add_edge("output_finalization", END)
    
    # Compile graph
    return workflow.compile()

# Compile default graph for module-level usage and tests compatibility
compiled_graph = create_pipeline(mode="standard")

# 3. Visualize Graph Function
def visualize_graph(graph, filename="graph_flow.png"):
    try:
        logger.info("Generating graph visualization...")
        png_bytes = graph.get_graph().draw_mermaid_png()
        output_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), filename)
        with open(output_path, "wb") as f:
            f.write(png_bytes)
        logger.info("Graph visualization saved successfully", path=output_path)
        print(f"\n[SUCCESS] Graph visualization saved to {output_path}")
    except Exception as e:
        logger.error("Failed to generate graph visualization", error=str(e))
        print(f"\n[WARNING] Could not generate graph visualization: {e}")

# 4. Self-execution for verification
if __name__ == "__main__":
    print("\n--- Running compiled StateGraph verification ---\n")
    
    # Generate visualization
    visualize_graph(compiled_graph)
    
    # We will test all three paths by changing the candidate profile's test score
    test_scores = [9.0, 7.0, 4.0]
    paths = ["fast_track", "standard", "gap_focus"]
    
    for score, path_name in zip(test_scores, paths):
        print(f"\nTesting Path: {path_name.upper()} (Forced score: {score})")
        initial_state: JobCrewState = {
            "candidate_profile": {
                "name": "Jane Doe",
                "experience": "5 years Python developer",
                "test_fit_score": score
            },
            "job_description": "Senior Software Engineer seeking Python & LangChain expertise.",
            "job_source": "USAJobs",
            "job_country": "US",
            "job_analysis": None,
            "fit_score": None,
            "execution_path": None,
            "execution_path_reason": None,
            "resume_output": None,
            "messaging_output": None,
            "interview_prep_output": None,
            "skills_gap_output": None,
            "company_intel_output": None,
            "rag_metadata": {},
            "quality_scores": {},
            "execution_metadata": None,
            "status": "started"
        }
        
        # Configure metadata for LangSmith tracing
        config = {
            "metadata": {
                "job_title": "Senior Software Engineer",
                "country": "US",
                "pipeline_version": settings.pipeline_version,
                "forced_test_score": score
            }
        }
        
        final_state = compiled_graph.invoke(initial_state, config=config)
        
        print(f"Status: {final_state['status']}")
        exec_meta = final_state.get("execution_metadata")
        if exec_meta:
            print(f"Nodes executed in order: {' -> '.join(exec_meta.nodes_executed)}")
            print(f"Path reason: {final_state.get('execution_path_reason')}")
            print(f"Primary provider used: {exec_meta.provider_used}")
            print(f"Errors recorded: {exec_meta.errors}")
