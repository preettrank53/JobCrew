import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="JobCrew - AI Job Application Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_header():
    st.markdown("<h1 style='text-align: center;'>JobCrew</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Your AI-powered job application assistant - powered by CrewAI & Groq</h4>", unsafe_allow_html=True)
    st.divider()

def initialize_session_state():
    if "jobs" not in st.session_state:
        st.session_state.jobs = []
    if "selected_jobs" not in st.session_state:
        st.session_state.selected_jobs = []
    if "candidate_profile" not in st.session_state:
        st.session_state.candidate_profile = {}
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "pipeline_running" not in st.session_state:
        st.session_state.pipeline_running = False
    if "viewing_application" not in st.session_state:
        st.session_state.viewing_application = None
    if "editing_status" not in st.session_state:
        st.session_state.editing_status = None
    if "tracker_summary" not in st.session_state:
        st.session_state.tracker_summary = None
    if "refresh_tracker" not in st.session_state:
        st.session_state.refresh_tracker = False

def render_workflow_guide():
    if not st.session_state.get("candidate_profile"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Step 1 - Fill your candidate profile in the sidebar")
        with col2:
            st.info("Step 2 - Search and select target job positions")
        with col3:
            st.info("Step 3 - Run the pipeline to generate materials")
