from crewai import Task

def create_messaging_task(agent, candidate_profile, job_data):
    return Task(
        description=f"""Using the candidate profile and the job analysis provided below, produce output in exactly these labeled sections:
- ## LINKEDIN MESSAGE — the actual outreach message, strictly under 300 words, with a personalized opening referencing the specific department and role, a middle section connecting the candidate's background to the mission, and a closing with one specific question or call to action
- ## SUBJECT LINE — a concise compelling connection request note under 200 characters
- ## FOLLOW-UP MESSAGE — a short follow-up message to send if no response after one week, under 150 words

CRITICAL INSTRUCTION: Avoid generic phrases like "I came across your posting" — every sentence must reference a specific detail from the job data injected into the prompt.

Candidate Profile:
{candidate_profile}

Job Data:
{job_data}
""",
        expected_output="A LinkedIn message, subject line, and follow-up message formatted exactly as requested.",
        agent=agent
    )
