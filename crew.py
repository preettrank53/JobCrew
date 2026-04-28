import time
import concurrent.futures
from crewai import Crew, Process
from agents import create_job_analyzer_agent, create_resume_customizer_agent, create_messaging_agent, create_interview_prep_agent
from tasks import create_job_analysis_task, create_resume_task, create_messaging_task, create_interview_prep_task
from config.settings import PIPELINE_TIMEOUT_SECONDS
from config.llm import get_user_llm
from demo.demo_controller import is_demo_mode

def run_jobcrew_pipeline(job_data, candidate_profile, fast_mode=False):
    # Safety guard: prevent real API calls during demo sessions
    if is_demo_mode():
        raise RuntimeError("Pipeline called in demo mode — use run_demo_pipeline instead")

    # Step 1: Resolve the user LLM (raises ValueError if no key is configured)
    user_llm = get_user_llm(fast_mode=fast_mode)

    # Step 2: Instantiate agents with user key
    job_analyzer = create_job_analyzer_agent(fast_mode=fast_mode, llm=user_llm)
    resume_customizer = create_resume_customizer_agent(fast_mode=fast_mode, llm=user_llm)
    messaging_agent = create_messaging_agent(fast_mode=fast_mode, llm=user_llm)
    interview_prep_agent = create_interview_prep_agent(fast_mode=fast_mode, llm=user_llm)
    
    # Step 2: Instantiate tasks in order
    task1 = create_job_analysis_task(agent=job_analyzer, job_data=job_data)
    
    # Passing context explicitly via property to use CrewAI context passing
    task2 = create_resume_task(
        agent=resume_customizer, 
        job_analysis_output="See provided context", 
        candidate_profile=candidate_profile
    )
    task2.context = [task1]
    
    task3 = create_messaging_task(
        agent=messaging_agent,
        job_data=job_data,
        candidate_profile=candidate_profile
    )

    task4 = create_interview_prep_task(
        agent=interview_prep_agent,
        job_analysis_output="See provided context",
        candidate_profile=candidate_profile
    )
    task4.context = [task1]
    
    # Step 3: Create a Crew instance
    crew = Crew(
        agents=[job_analyzer, resume_customizer, messaging_agent, interview_prep_agent],
        tasks=[task1, task2, task3, task4],
        verbose=True,
        process=Process.sequential
    )
    
    # Step 4: Execute with timeout and timing
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(crew.kickoff)
        try:
            future.result(timeout=PIPELINE_TIMEOUT_SECONDS)
        except concurrent.futures.TimeoutError:
            raise RuntimeError(
                f"Pipeline timed out after {PIPELINE_TIMEOUT_SECONDS} seconds "
                f"-- try fast mode or reduce selected jobs"
            )
    
    end_time = time.time()
    execution_time_seconds = round(end_time - start_time, 2)
    
    # Extract raw string outputs from each task
    job_analysis = task1.output.raw if task1.output else "No output generated"
    resume_and_cover_letter = task2.output.raw if task2.output else "No output generated"
    linkedin_message = task3.output.raw if task3.output else "No output generated"
    interview_prep = task4.output.raw if task4.output else "No output generated"
    
    return {
        "job_analysis": job_analysis,
        "resume_and_cover_letter": resume_and_cover_letter,
        "linkedin_message": linkedin_message,
        "interview_prep": interview_prep,
        "job_title": job_data.get("title", "Unknown Title"),
        "department": job_data.get("department", "Unknown Department"),
        "execution_time_seconds": execution_time_seconds
    }

if __name__ == "__main__":
    from tools import fetch_jobs
    import sys
    
    print("Fetching sample job...")
    try:
        jobs = fetch_jobs("data analyst", results_per_page=1)
    except Exception as e:
        print(f"Error fetching job: {e}")
        sys.exit(1)
        
    if not jobs:
        print("No jobs found to test the pipeline.")
    else:
        sample_job = jobs[0]
        
        sample_candidate = {
            "name": "Alex Mercer",
            "experience": "4 years of experience analyzing large datasets, building dashboards in Tableau, and writing complex SQL queries. Previous role as Data Analyst II at TechCorp.",
            "skills": ["SQL", "Python", "Tableau", "Data Modeling", "Communication"],
            "education": "B.S. in Data Science from State University"
        }
        
        print(f"Starting JobCrew pipeline for role: {sample_job.get('title')}...")
        try:
            results = run_jobcrew_pipeline(sample_job, sample_candidate)
            
            print("\n" + "="*50)
            print(f"PIPELINE COMPLETED FOR: {results['job_title']} at {results['department']}")
            print(f"Execution Time: {results['execution_time_seconds']}s")
            print("="*50)
            print("\n[JOB ANALYSIS RESULT]\n")
            print(results['job_analysis'])
            print("\n" + "="*50)
            print("\n[RESUME & COVER LETTER RESULT]\n")
            print(results['resume_and_cover_letter'])
            print("\n" + "="*50)
            print("\n[LINKEDIN MESSAGE RESULT]\n")
            print(results['linkedin_message'])
            print("\n" + "="*50)
        except Exception as e:
            print(f"Pipeline execution failed: {e}")
