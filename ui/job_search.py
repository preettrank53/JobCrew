import streamlit as st
from tools import fetch_jobs, clear_jobs_cache, get_cache_stats
from demo.demo_controller import is_demo_mode


def render_job_search_panel():
    # Demo Mode: skip profile check, skip search controls, render pre-loaded listings
    if is_demo_mode():
        st.success("Demo profile loaded — Alex Johnson, Data Scientist")
        st.caption("Demo: Showing 3 sample job listings — exit demo mode to search real jobs")
        _render_job_listings()
        return

    if not st.session_state.get("candidate_profile"):
        st.warning("Please complete your candidate profile in the sidebar before searching for jobs.")
        return

    st.header("Search Government Jobs")
    
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        keyword = st.text_input("Keyword", placeholder="e.g. data analyst, software engineer")
    with col2:
        location = st.text_input("Location", placeholder="e.g. Washington DC")
    with col3:
        results_per_page = st.number_input("Results per page", min_value=5, max_value=25, value=10)
        
    with st.expander("Cache Status"):
        st.json(get_cache_stats())
        
    if st.button("Fetch Jobs", use_container_width=True):
        if not keyword.strip():
            st.warning("Please enter a keyword to search.")
        else:
            with st.spinner("Fetching live jobs from USAJobs..."):
                try:
                    jobs = fetch_jobs(keyword=keyword, location=location, results_per_page=results_per_page)
                    if not jobs:
                        st.warning("No jobs found. Try a broader keyword or remove the location filter.")
                    else:
                        st.session_state.jobs = jobs
                        st.session_state.selected_jobs = []
                        for key in list(st.session_state.keys()):
                            if key.startswith("check_"):
                                del st.session_state[key]
                        st.success(f"Successfully fetched {len(jobs)} jobs.")
                except Exception as e:
                    st.error(f"Error fetching jobs: {str(e)}")

    if not st.session_state.get("jobs"):
        st.markdown(
            "<p style='text-align: center; color: gray; margin-top: 2rem;'>"
            "No jobs to display. Use the search bar above to find target positions.</p>",
            unsafe_allow_html=True,
        )
    else:
        _render_job_listings()

    if st.session_state.get("jobs"):
        if st.button("Clear Results"):
            st.session_state.jobs = []
            st.session_state.selected_jobs = []
            for key in list(st.session_state.keys()):
                if key.startswith("check_"):
                    del st.session_state[key]
            st.rerun()
        if st.button("Clear API Cache"):
            clear_jobs_cache()
            st.success("API cache cleared")
            st.rerun()


def _render_job_listings():
    """Renders the available positions listing from session state (shared by live and demo paths)."""
    st.header("Available Positions")
    st.write(f"Total jobs fetched: {len(st.session_state.jobs)}")

    current_selected = []

    for job in st.session_state.jobs:
        job_id = job.get("job_id", "Unknown_ID")
        title = job.get("title", "Unknown Title")
        department = job.get("department", "Unknown Department")

        with st.expander(f"{department} - {title}"):
            c1, c2 = st.columns(2)
            with c1:
                st.write(f"**Department:** {department}")
                st.write(f"**Location:** {job.get('location', 'Not Specified')}")
                sal_min = job.get("salary_min", "0")
                sal_max = job.get("salary_max", "0")
                st.write(f"**Salary Range:** ${sal_min} - ${sal_max}")
            with c2:
                st.write(f"**Close Date:** {job.get('close_date', 'Not Specified')}")
                st.write(f"**Job ID:** {job_id}")
                url = job.get("apply_url", "#")
                st.markdown(f"[Apply URL]({url})")

            st.markdown("**Description:**")
            st.markdown(job.get("description", "No description provided."))

            is_checked = st.checkbox("Select this position", key=f"check_{job_id}")
            if is_checked:
                current_selected.append(job)

    st.session_state.selected_jobs = current_selected

    if st.session_state.get("selected_jobs"):
        st.info(f"Selected Positions: {len(st.session_state.selected_jobs)}")
        for job in st.session_state.selected_jobs:
            st.markdown(f"- {job.get('title', 'Unknown')}")
