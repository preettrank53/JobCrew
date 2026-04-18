from crewai import Agent
from config.llm import llm, get_fast_llm
from config.settings import MAX_AGENT_ITERATIONS, MAX_AGENT_RPM

def create_resume_customizer_agent(fast_mode=False):
    agent_llm = get_fast_llm() if fast_mode else llm
    agent_max_iter = 2 if fast_mode else MAX_AGENT_ITERATIONS
    
    return Agent(
        role='Federal Resume Specialist',
        goal='Produce a tailored resume summary and a compelling cover letter that scores above 85% on ATS keyword matching, follows federal application writing conventions, and makes the hiring manager want to schedule an interview.',
        backstory='You are a certified Professional Resume Writer with 12 years of experience specializing in federal and government contractor applications, have helped over 500 candidates successfully land GS-level positions, and understand exactly how to map candidate experience to OPM competency frameworks.',
        verbose=True,
        allow_delegation=False,
        llm=agent_llm,
        memory=False,
        max_iter=agent_max_iter,
        max_rpm=MAX_AGENT_RPM
    )
