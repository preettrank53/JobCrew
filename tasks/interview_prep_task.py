from crewai import Task

def create_interview_prep_task(agent, job_analysis_output, candidate_profile, job_data):
    return Task(
        description=f"""
Review the following job analysis, candidate profile, and job details carefully.

Job Title: {job_data.get('title')}
Department: {job_data.get('department')}
Job Description: {job_data.get('description')}

Job Analysis Output:
{job_analysis_output}

Candidate Profile:
Name: {candidate_profile.get('name')}
Experience: {candidate_profile.get('experience')}
Skills: {candidate_profile.get('skills')}
Education: {candidate_profile.get('education')}

Your task is to generate exactly 10 interview questions distributed across these four categories:
1. 3 Technical/Skills questions based on the mandatory requirements and critical keywords from the job analysis.
2. 3 Behavioral questions using the STAR method based on the key responsibilities from the job analysis.
3. 2 Situational questions based on culture and environment signals from the job analysis.
4. 2 Role-specific questions that only someone who carefully read this exact job posting would ask.

For each question, generate a personalized answer framework that:
- Uses the candidate's actual experience, skills, and background — not generic advice.
- References specific details from their work history where relevant.
- Follows STAR format for behavioral questions.
- Gives concrete talking points not vague suggestions.

CRITICAL INSTRUCTION: Do not invent experience not present in the candidate profile — only use what is actually there.
""",
        expected_output="""\
## INTERVIEW PREPARATION REPORT
## TECHNICAL QUESTIONS (3)
### Question 1: [question text]
**Why they ask this:** [one sentence]
**Your Answer Framework:** [personalized framework using candidate's actual experience]
**Key Points to Hit:** [3 bullet points]
### Question 2: ...
### Question 3: ...
## BEHAVIORAL QUESTIONS (3)
### Question 4: [question text]
**Why they ask this:** [one sentence]
**STAR Framework:**
- Situation: [specific situation from candidate's background]
- Task: [what they were responsible for]
- Action: [specific actions they took]
- Result: [quantifiable outcome if possible]
### Question 5: ...
### Question 6: ...
## SITUATIONAL QUESTIONS (2)
### Question 7: [question text]
**Why they ask this:** [one sentence]
**Suggested Approach:** [how to frame the answer given this department's culture]
### Question 8: ...
## ROLE-SPECIFIC QUESTIONS (2)
### Question 9: [question text]
**Why they ask this:** [one sentence]
**Key Points to Hit:** [2-3 bullet points]
### Question 10: ...
## INTERVIEW STRATEGY SUMMARY
[3-4 sentences on overall positioning strategy for this specific role and department]
""",
        agent=agent
    )
