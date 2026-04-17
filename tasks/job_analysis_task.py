import json
from crewai import Task

def create_job_analysis_task(agent, job_data):
    job_data_str = json.dumps(job_data, indent=2)
    
    return Task(
        description=(
            "Analyze the following job listing data thoroughly.\n\n"
            f"Job Data:\n{job_data_str}\n\n"
            "Extract the following information:\n"
            "1. Required skills\n"
            "2. Preferred qualifications\n"
            "3. Key responsibilities\n"
            "4. Experience level\n"
            "5. Education requirements\n"
            "6. Department culture signals"
        ),
        expected_output=(
            "A clearly structured plain text report with labeled sections for each extracted category:\n"
            "- Required Skills\n"
            "- Preferred Qualifications\n"
            "- Key Responsibilities\n"
            "- Experience Level\n"
            "- Education Requirements\n"
            "- Department Culture Signals"
        ),
        agent=agent
    )
