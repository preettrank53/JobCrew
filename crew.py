from crewai import Crew, Process
from agents import create_job_analyzer_agent, create_resume_customizer_agent, create_messaging_agent
from tasks import create_job_analysis_task, create_resume_task, create_messaging_task

def run_jobcrew_pipeline(job_data, candidate_profile):
    # Step 1: Instantiate agents
    job_analyzer = create_job_analyzer_agent()
    resume_customizer = create_resume_customizer_agent()
    messaging_agent = create_messaging_agent()
    
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
    
    # Step 3: Create a Crew instance
    crew = Crew(
        agents=[job_analyzer, resume_customizer, messaging_agent],
        tasks=[task1, task2, task3],
        verbose=True,
        process=Process.sequential
    )
    
    # Step 4: Execute and return results
    crew.kickoff()
    
    # Extract raw string outputs from each task
    job_analysis = task1.output.raw if task1.output else "No output generated"
    resume_and_cover_letter = task2.output.raw if task2.output else "No output generated"
    linkedin_message = task3.output.raw if task3.output else "No output generated"
    
    return {
        "job_analysis": job_analysis,
        "resume_and_cover_letter": resume_and_cover_letter,
        "linkedin_message": linkedin_message,
        "job_title": job_data.get("title", "Unknown Title"),
        "department": job_data.get("department", "Unknown Department")
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
