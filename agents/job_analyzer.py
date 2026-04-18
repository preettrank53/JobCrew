from crewai import Agent
from config.llm import llm, get_fast_llm
from config.settings import MAX_AGENT_ITERATIONS, MAX_AGENT_RPM

def create_job_analyzer_agent(fast_mode=False):
    agent_llm = get_fast_llm() if fast_mode else llm
    agent_max_iter = 2 if fast_mode else MAX_AGENT_ITERATIONS
    
    return Agent(
        role='Senior Federal Job Analyst',
        goal='Extract a comprehensive structured breakdown that gives a resume writer everything they need to tailor application materials with zero ambiguity.',
        backstory='You have spent 15 years in federal HR and talent acquisition, have reviewed over 10,000 USAJobs postings, understand OPM qualification standards, and know exactly how to identify the difference between mandatory and preferred requirements in government job postings.',
        verbose=True,
        allow_delegation=False,
        llm=agent_llm,
        memory=False,
        max_iter=agent_max_iter,
        max_rpm=MAX_AGENT_RPM
    )
