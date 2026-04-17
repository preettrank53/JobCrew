import json
from crewai import Task

def create_resume_task(agent, job_analysis_output, candidate_profile):
    candidate_profile_str = json.dumps(candidate_profile, indent=2)
    
    return Task(
        description=(
            "Using the provided job analysis and candidate profile, create tailored application materials.\n\n"
            f"Job Analysis Output:\n{job_analysis_output}\n\n"
            f"Candidate Profile:\n{candidate_profile_str}\n\n"
            "You must generate two clearly separated sections:\n"
            "1. A tailored resume summary paragraph optimized for the analyzed job requirements.\n"
            "2. A full professional cover letter addressed to the hiring department, highlighting how "
            "the candidate's experience specifically matches the role's needs."
        ),
        expected_output=(
            "A structured plain text document with two clear sections:\n"
            "--- RESUME SUMMARY ---\n"
            "[Tailored summary paragraph]\n\n"
            "--- COVER LETTER ---\n"
            "[Full professional cover letter]"
        ),
        agent=agent
    )
