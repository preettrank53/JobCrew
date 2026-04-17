import streamlit as st
from tools import fetch_jobs

def render_job_search_panel():
    st.header("Search Government Jobs")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        keyword = st.text_input("Keyword", placeholder="e.g. data analyst, software engineer")
    with col2:
        location = st.text_input("Location", placeholder="e.g. Washington DC")
    with col3:
        results_per_page = st.number_input("Results per page", min_value=5, max_value=25, value=10)
        
    if st.button("Fetch Jobs", use_container_width=True):
        if not keyword.strip():
            st.warning("Please enter a keyword to search.")
        else:
            with st.spinner("Fetching live jobs from USAJobs..."):
                try:
                    jobs = fetch_jobs(keyword=keyword, location=location, results_per_page=results_per_page)
                    st.session_state.jobs = jobs
                    # Reset selected jobs
                    st.session_state.selected_jobs = []
                    # Clear checkbox states
                    for key in list(st.session_state.keys()):
                        if key.startswith("check_"):
                            del st.session_state[key]
                    st.success(f"Successfully fetched {len(jobs)} jobs.")
                except Exception as e:
                    st.error(f"Error fetching jobs: {str(e)}")

    if st.session_state.jobs:
        st.header("Available Positions")
        st.write(f"Total jobs fetched: {len(st.session_state.jobs)}")
        
        current_selected = []
        
        for job in st.session_state.jobs:
            job_id = job.get('job_id', 'Unknown_ID')
            title = job.get('title', 'Unknown Title')
            department = job.get('department', 'Unknown Department')
            
            with st.expander(f"{department} - {title}"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Department:** {department}")
                    st.write(f"**Location:** {job.get('location', 'Not Specified')}")
                    sal_min = job.get('salary_min', '0')
                    sal_max = job.get('salary_max', '0')
                    st.write(f"**Salary Range:** ${sal_min} - ${sal_max}")
                with c2:
                    st.write(f"**Close Date:** {job.get('close_date', 'Not Specified')}")
                    st.write(f"**Job ID:** {job_id}")
                    url = job.get('apply_url', '#')
                    st.markdown(f"[Apply URL]({url})")
                
                st.markdown("**Description:**")
                st.markdown(job.get('description', 'No description provided.'))
                
                is_checked = st.checkbox("Select this position", key=f"check_{job_id}")
                if is_checked:
                    current_selected.append(job)
                    
        st.session_state.selected_jobs = current_selected

    if st.session_state.selected_jobs:
        st.info(f"Selected Positions: {len(st.session_state.selected_jobs)}")
        for job in st.session_state.selected_jobs:
            st.markdown(f"- {job.get('title', 'Unknown')}")
