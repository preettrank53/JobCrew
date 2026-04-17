from crewai import Agent
from config.llm import llm

def create_messaging_agent():
    return Agent(
        role='Professional Networking Coach',
        goal='Craft a LinkedIn outreach message that feels genuinely human, references specific details about the role and department, establishes a clear reason for connecting, and has a single low-friction call to action that gets a response.',
        backstory='You are a professional networking coach who has studied thousands of LinkedIn cold outreach messages, knows the exact psychological triggers that make recruiters respond, and specializes in government and public sector professional networking.',
        verbose=True,
        allow_delegation=False,
        llm=llm,
        memory=False,
        max_rpm=10
    )
