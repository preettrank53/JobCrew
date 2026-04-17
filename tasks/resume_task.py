from crewai import Task

def create_resume_task(agent, candidate_profile, job_analysis_output="See provided context"):
    return Task(
        description=f"""Using the candidate profile and the job analysis provided below, produce output in exactly these labeled sections:
- ## TAILORED RESUME SUMMARY — a three to four sentence professional summary paragraph that directly mirrors the job's critical keywords and requirements, written in first person
- ## KEY QUALIFICATIONS SECTION — six to eight bullet points mapping the candidate's specific experience and skills directly to the job's mandatory requirements
- ## COVER LETTER — a full professional cover letter with four paragraphs: opening hook referencing the specific role and department, body paragraph one mapping experience to requirements, body paragraph two demonstrating cultural fit and mission alignment, closing paragraph with a clear call to action
- ## ATS KEYWORD CHECKLIST — a list of critical keywords from the job analysis and whether each one appears in the generated materials

CRITICAL INSTRUCTION: Do not invent experience or qualifications not present in the candidate profile — only reframe and emphasize what is already there.

Candidate Profile:
{candidate_profile}

Job Analysis Context:
{job_analysis_output}
""",
        expected_output="A tailored resume summary, key qualifications section, cover letter, and ATS keyword checklist formatted exactly as requested.",
        agent=agent
    )
