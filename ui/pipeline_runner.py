import streamlit as st
import os
import datetime
import time
from crew import run_jobcrew_pipeline
from tools.output_formatter import format_output_for_display, format_output_for_download, calculate_quality_indicators
from tracker.log_reader import invalidate_applications_cache
import streamlit.components.v1 as components

def save_results_to_log(job_id, result, candidate_name):
    if not os.path.exists('logs'):
        os.makedirs('logs')
        
    log_path = os.path.join('logs', f"log_{job_id}.txt")
    
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(format_output_for_download(result, candidate_name))
    invalidate_applications_cache()

def render_pipeline_runner():
    st.header("Generate Application Materials")

    # Guard: require API key before proceeding
    if not st.session_state.get("user_llm_key", "").strip():
        st.warning("Please configure your LLM API key in the sidebar before running the pipeline.")
        return

    selected_jobs = st.session_state.get('selected_jobs', [])
    profile = st.session_state.get('candidate_profile', {})
    candidate_name = profile.get('name', 'Applicant')

    missing_jobs = not selected_jobs
    missing_profile = not profile or not all(k in profile for k in ['name', 'experience', 'skills', 'education'])

    if missing_jobs:
        st.warning("Missing: Please select at least one job from the 'Available Positions' list above.")

    if missing_profile:
        st.warning("Missing: Please complete and save your Candidate Profile in the sidebar.")

    if st.session_state.get('pipeline_running', False):
        st.warning("Pipeline is already running — please wait for it to complete")
        return


    if not missing_jobs and not missing_profile:
        fast_mode = st.toggle("Fast Mode (quicker results, slightly less detail)", key="fast_mode_toggle")
        st.caption("Fast mode uses lower token limits and fewer iterations -- recommended for testing")
        
        if st.button("Run JobCrew Pipeline", use_container_width=True):
            st.session_state.pipeline_running = True
            all_successful = True
            
            start_time = time.time()
            progress_bar = st.progress(0)
            total_jobs = len(selected_jobs)
            current_job_index = 0
            
            try:
                for job in selected_jobs:
                    job_id = job.get('job_id', 'unknown')
                    job_title = job.get('title', 'Unknown Title')
                    
                    with st.status(f"Processing: {job_title}", expanded=True) as status:
                        try:
                            st.write("Analyzing job requirements...")
                            st.write("Tailoring resume and cover letter...")
                            st.write("Drafting LinkedIn message...")
                            
                            result = run_jobcrew_pipeline(job_data=job, candidate_profile=profile, fast_mode=fast_mode)
                            st.session_state.results[job_id] = result
                            save_results_to_log(job_id, result, candidate_name)
                            
                            exec_time = result.get('execution_time_seconds', 0)
                            status.update(label=f"Completed: {job_title}", state="complete", expanded=False)
                            st.caption(f"Completed in {exec_time}s")
                        except Exception as e:
                            status.update(label=f"Error processing {job_title}", state="error", expanded=False)
                            st.error(f"Pipeline error: {str(e)}")
                            all_successful = False
                            
                    current_job_index += 1
                    progress_bar.progress(current_job_index / total_jobs)
            except Exception as global_e:
                st.error("An unexpected global error occurred during pipeline execution.")
                with st.expander("Error Details"):
                    st.write(str(global_e))
                all_successful = False
            
            st.session_state.pipeline_running = False
            
            end_time = time.time()
            progress_bar.progress(1.0)
            st.success("All jobs processed successfully")
            st.caption(f"Pipeline completed in {end_time - start_time:.1f} seconds")
            
            if all_successful and selected_jobs:
                st.balloons()

    if not st.session_state.get('results') and not st.session_state.get('pipeline_running', False):
        st.markdown("<p style='text-align: center; color: gray; margin-top: 2rem;'>No results yet - select jobs and run the pipeline to generate your application materials.</p>", unsafe_allow_html=True)

    if st.session_state.get('results'):
        st.header("Generated Application Materials")
        
        for job_id, result in st.session_state.results.items():
            st.subheader(f"{result.get('job_title', 'Unknown')} - {result.get('department', 'Unknown')}")
            
            indicators = calculate_quality_indicators(result)
            i1, i2, i3 = st.columns(3)
            i1.info(f"Job Analysis Quality: **{indicators['analysis_quality']['label']}**")
            i2.info(f"Resume Quality: **{indicators['resume_quality']['label']}**")
            i3.info(f"Messaging Quality: **{indicators['messaging_quality']['label']}**")
            
            tab1, tab2, tab3 = st.tabs(["Job Analysis", "Resume & Cover Letter", "LinkedIn Message"])
            
            with tab1:
                display_analysis = format_output_for_display(result.get('job_analysis', ''), 'analysis')
                st.markdown(display_analysis)
                st.caption(f"Quality: {indicators['analysis_quality']['score']}/{indicators['analysis_quality']['max_score']} sections detected")
                
            with tab2:
                display_resume = format_output_for_display(result.get('resume_and_cover_letter', ''), 'resume')
                st.markdown(display_resume)
                st.caption(f"Quality: {indicators['resume_quality']['score']}/{indicators['resume_quality']['max_score']} checks passed")
                
                full_download = format_output_for_download(result, candidate_name)
                st.download_button(
                    label="Download All Materials",
                    data=full_download,
                    file_name=f"jobcrew_{candidate_name.replace(' ', '_')}_{job_id}.txt",
                    mime="text/plain",
                    key=f"dl_all_{job_id}"
                )
                
            with tab3:
                display_msg = format_output_for_display(result.get('linkedin_message', ''), 'messaging')
                st.markdown(display_msg)
                st.caption(f"Quality: {indicators['messaging_quality']['score']}/{indicators['messaging_quality']['max_score']} checks passed")
                
                if st.button("Copy to Clipboard", key=f"copy_{job_id}"):
                    safe_msg = display_msg.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')
                    js = f"<script>navigator.clipboard.writeText(`{safe_msg}`);</script>"
                    components.html(js, height=0, width=0)
                    st.success("Copied to clipboard!")
                
        if st.button("Clear All Results"):
            st.session_state.results = {}
            st.rerun()
