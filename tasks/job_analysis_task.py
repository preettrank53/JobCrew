from crewai import Task

def create_job_analysis_task(agent, job_data):
    return Task(
        description=f"""Analyze the following federal job description and produce output in exactly these labeled sections:
- ## POSITION OVERVIEW — job title, department, grade level, location, salary range, closing date
- ## MANDATORY REQUIREMENTS — education, experience, certifications listed as bullet points
- ## PREFERRED QUALIFICATIONS — nice-to-have skills and experience as bullet points
- ## KEY RESPONSIBILITIES — top five to seven duties extracted from the description
- ## CRITICAL KEYWORDS — ATS-relevant keywords and phrases the resume must contain
- ## CULTURE & ENVIRONMENT SIGNALS — tone, team size hints, mission focus, work style indicators
- ## APPLICATION STRATEGY — two to three sentences on how to position the candidate for this specific role

Job Data:
{job_data}
""",
        expected_output="A structured markdown report with all seven sections populated, no section left empty, using only information found in the provided job data.",
        agent=agent
    )
