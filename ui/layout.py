import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="JobCrew - AI Job Application Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_header():
    st.markdown("<h1 style='text-align: center;'>JobCrew</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: gray;'>Your AI-powered job application assistant - powered by CrewAI & Google Gemini</h4>", unsafe_allow_html=True)
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
