import json
from crewai import Task

def create_messaging_task(agent, job_data, candidate_profile):
    job_data_str = json.dumps(job_data, indent=2)
    candidate_profile_str = json.dumps(candidate_profile, indent=2)
    
    role_title = job_data.get('title', 'the open role')
    department = job_data.get('department', 'your department')
    
    return Task(
        description=(
            f"Draft a concise LinkedIn outreach message regarding the '{role_title}' position in the '{department}'.\n\n"
            f"Job Listing Details:\n{job_data_str}\n\n"
            f"Candidate Profile:\n{candidate_profile_str}\n\n"
            "Write a highly personalized, professional LinkedIn message (under 300 words). "
            "The message should reference the specific role, the department, and express a genuine reason for interest "
            "based on the candidate's profile. End with a polite call to action for a brief chat."
        ),
        expected_output="A single plain text LinkedIn outreach message under 300 words.",
        agent=agent
    )
