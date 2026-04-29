from crewai import Agent
from config.llm import get_user_llm

def create_interview_prep_agent(fast_mode=False, llm=None):
    if llm is None:
        try:
            llm = get_user_llm(fast_mode=fast_mode)
        except Exception:
            from config.llm import llm as fallback_llm
            llm = fallback_llm

    return Agent(
        role="Senior Technical Interview Coach and Career Strategist",
        goal="Analyze job requirements alongside the candidate's background to generate highly specific, realistic interview questions with personalized answer frameworks that give the candidate a genuine competitive advantage in interviews for this exact role",
        backstory=(
            "You are a former hiring manager with 12 years of experience across federal agencies and private sector tech companies. "
            "You have conducted over 800 technical interviews, know exactly what interviewers at each department type are looking for, "
            "and specialize in helping candidates turn their existing experience into compelling, confident interview answers using structured storytelling frameworks."
        ),
        verbose=True,
        allow_delegation=False,
        memory=False,
        llm=llm,
        max_iter=2 if fast_mode else 3,
        max_rpm=10
    )
