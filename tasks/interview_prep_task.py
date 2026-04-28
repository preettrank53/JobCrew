from crewai import Task


def create_interview_prep_task(agent, job_analysis_output, candidate_profile):
    return Task(
        description=f"""Read the job analysis and the candidate profile below.
Write a practical interview preparation guide in simple, easy-to-understand English.
Do not use complicated words. Write as if you are helping a friend prepare for their interview.

Produce output in exactly these five sections:

## LIKELY INTERVIEW QUESTIONS
Write 8 questions the interviewer will most likely ask, based on the job requirements.
Make the questions specific to this role, not generic questions like "tell me about yourself".

## SUGGESTED ANSWERS
For each of the 8 questions above, write a short answer guide using the STAR method:
- Situation: what was happening
- Task: what the candidate needed to do
- Action: what steps the candidate took
- Result: what happened because of those actions
Use the candidate's actual experience from their profile to make the answers real and specific.
Keep each answer guide short and easy to remember.

## TECHNICAL TOPICS TO PREPARE
List 5 technical areas the candidate should study or review before the interview.
For each topic, write one sentence explaining why this topic is important for this specific job.
Keep it simple and actionable.

## BEHAVIOURAL COMPETENCIES
List 3 key qualities the employer is looking for based on the job description.
For each quality, write one example story from the candidate's background that shows this quality.
Keep the examples short and clear.

## RED FLAGS TO ADDRESS
Identify 2 to 3 possible weak points or gaps in the candidate's profile that the interviewer might ask about.
For each gap, write a short, honest, and confident way to answer if the interviewer brings it up.
Do not suggest the candidate lie. Help them frame the truth in a positive way.

Job Analysis:
{job_analysis_output}

Candidate Profile:
{candidate_profile}
""",
        expected_output=(
            "A structured interview preparation guide with all five sections fully filled in, "
            "written in simple and clear English. Each section must have real, specific content "
            "based on the job and the candidate — no generic advice."
        ),
        agent=agent
    )
