from crewai import Agent
from config.llm import get_llm, get_fast_llm
from config.settings import MAX_AGENT_ITERATIONS, MAX_AGENT_RPM

def create_messaging_agent(fast_mode=False, llm=None):
    agent_llm = llm if llm else (get_fast_llm() if fast_mode else get_llm())
    agent_max_iter = 2 if fast_mode else MAX_AGENT_ITERATIONS
    
    return Agent(
        role='Professional Networking Coach',
        goal='Craft a LinkedIn outreach message that feels genuinely human, references specific details about the role and department, establishes a clear reason for connecting, and has a single low-friction call to action that gets a response.',
        backstory='You are a professional networking coach who has studied thousands of LinkedIn cold outreach messages, knows the exact psychological triggers that make recruiters respond, and specializes in government and public sector professional networking.',
        verbose=True,
        allow_delegation=False,
        llm=agent_llm,
        memory=False,
        max_iter=agent_max_iter,
        max_rpm=MAX_AGENT_RPM
    )
