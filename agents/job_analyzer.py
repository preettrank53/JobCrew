from crewai import Agent
from config.llm import llm

def create_job_analyzer_agent():
    return Agent(
        role="Senior Job Market Analyst",
        goal="Analyze job descriptions thoroughly and extract all key requirements, qualifications, skills, and responsibilities into a clean structured format",
        backstory=(
            "You are an experienced HR analyst and talent acquisition specialist. "
            "Having reviewed thousands of job postings, you understand exactly what hiring managers prioritize "
            "and can quickly dissect complex role descriptions into actionable insights."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
