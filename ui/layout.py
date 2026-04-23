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
    if "user_llm_key" not in st.session_state:
        st.session_state.user_llm_key = ""
    if "llm_provider" not in st.session_state:
        st.session_state.llm_provider = "Groq (Free & Fast - Recommended)"
    if "demo_mode" not in st.session_state:
        st.session_state.demo_mode = False
    if "demo_jobs_fetched" not in st.session_state:
        st.session_state.demo_jobs_fetched = False


def render_demo_banner():
    """Renders the demo-mode notice when Demo Mode is active."""
    from demo.demo_controller import is_demo_mode, get_demo_banner_html
    if is_demo_mode():
        st.warning(get_demo_banner_html())
        st.info(
            "This is a demo with sample data. To use your real resume and real jobs, "
            "exit demo mode and add your Groq API key - it is free at console.groq.com"
        )

def render_workflow_guide():
    if not st.session_state.get("candidate_profile"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("Step 1 - Fill your candidate profile in the sidebar")
        with col2:
            st.info("Step 2 - Search and select target job positions")
        with col3:
            st.info("Step 3 - Run the pipeline to generate materials")
