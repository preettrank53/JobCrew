from crewai import Agent
from config.llm import get_llm, get_fast_llm
from config.settings import MAX_AGENT_ITERATIONS, MAX_AGENT_RPM


def create_interview_prep_agent(fast_mode=False, llm=None):
    agent_llm = llm if llm else (get_fast_llm() if fast_mode else get_llm())
    agent_max_iter = 2 if fast_mode else MAX_AGENT_ITERATIONS

    return Agent(
        role="Senior Interview Coach",
        goal=(
            "Generate a clear and practical interview preparation guide based on the job "
            "requirements and the candidate's background, so the candidate knows exactly "
            "what to say and how to say it in the interview."
        ),
        backstory=(
            "You have 10 years of experience coaching people for government and private "
            "sector job interviews. You know the STAR method inside out — Situation, Task, "
            "Action, Result. You write in simple, clear English so candidates can easily "
            "remember and use your advice. You focus on what actually helps people get "
            "selected, not on generic tips they can find anywhere."
        ),
        verbose=True,
        allow_delegation=False,
        llm=agent_llm,
        memory=False,
        max_iter=agent_max_iter,
        max_rpm=MAX_AGENT_RPM
    )
