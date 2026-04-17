import streamlit as st
import os
import datetime
from crew import run_jobcrew_pipeline

def save_results_to_log(job_id, result):
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_path = os.path.join('logs', f"log_{job_id}.txt")
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Job Title: {result.get('job_title', 'Unknown')}\n")
        f.write(f"Department: {result.get('department', 'Unknown')}\n")
        f.write("\n" + "="*50 + "\n")
        f.write("JOB ANALYSIS\n")
        f.write("="*50 + "\n\n")
        f.write(result.get('job_analysis', ''))
        f.write("\n\n" + "="*50 + "\n")
        f.write("RESUME & COVER LETTER\n")
        f.write("="*50 + "\n\n")
        f.write(result.get('resume_and_cover_letter', ''))
        f.write("\n\n" + "="*50 + "\n")
        f.write("LINKEDIN MESSAGE\n")
        f.write("="*50 + "\n\n")
        f.write(result.get('linkedin_message', ''))

def render_pipeline_runner():
    st.header("Generate Application Materials")
    
    selected_jobs = st.session_state.get('selected_jobs', [])
    profile = st.session_state.get('candidate_profile', {})
    
    missing_jobs = not selected_jobs
    missing_profile = not profile or not all(k in profile for k in ['name', 'experience', 'skills', 'education'])
    
    if missing_jobs:
        st.warning("Missing: Please select at least one job from the 'Available Positions' list above.")
    
    if missing_profile:
        st.warning("Missing: Please complete and save your Candidate Profile in the sidebar (Name, Work Experience, Key Skills, and Education required).")
        
    if not missing_jobs and not missing_profile:
        if st.button("⚡Run JobCrew Pipeline", use_container_width=True):
            st.session_state.pipeline_running = True
            
            for job in selected_jobs:
                job_id = job.get('job_id', 'unknown')
                job_title = job.get('title', 'Unknown Title')
                
                with st.status(f"Processing: {job_title}", expanded=True) as status:
                    try:
                        st.write("Analyzing job requirements...")
                        st.write("Tailoring resume and cover letter...")
                        st.write("💬 Drafting LinkedIn message...")
                        
                        result = run_jobcrew_pipeline(job_data=job, candidate_profile=profile)
                        st.session_state.results[job_id] = result
                        save_results_to_log(job_id, result)
                        
                        status.update(label=f"Completed: {job_title}", state="complete", expanded=False)
                    except Exception as e:
                        status.update(label=f"Error processing {job_title}", state="error", expanded=False)
                        st.error(f"Pipeline error: {str(e)}")
            
            st.session_state.pipeline_running = False

    if st.session_state.get('results'):
        st.header("Generated Application Materials")
        
        for job_id, result in st.session_state.results.items():
            st.subheader(f"{result.get('job_title', 'Unknown')} — {result.get('department', 'Unknown')}")
            
            tab1, tab2, tab3 = st.tabs(["Job Analysis", "Resume & Cover Letter", "💬 LinkedIn Message"])
            
            with tab1:
                st.markdown(result.get('job_analysis', ''))
                
            with tab2:
                resume_content = result.get('resume_and_cover_letter', '')
                st.markdown(resume_content)
                st.download_button(
                    label="Download",
                    data=resume_content,
                    file_name=f"coverletter_{job_id}.txt",
                    mime="text/plain",
                    key=f"dl_resume_{job_id}"
                )
                
            with tab3:
                linkedin_content = result.get('linkedin_message', '')
                st.markdown(linkedin_content)
                st.download_button(
                    label="Download",
                    data=linkedin_content,
                    file_name=f"linkedin_{job_id}.txt",
                    mime="text/plain",
                    key=f"dl_linkedin_{job_id}"
                )
