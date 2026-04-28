"""
Demo Mode controller — manages activation, deactivation, simulated pipeline execution,
and UI helper utilities for Demo Mode.
"""

import time
import streamlit as st

from demo.demo_data import (
    DEMO_JOB,
    DEMO_CANDIDATE,
    DEMO_RESULTS,
    DEMO_JOBS_LIST,
)


# ---------------------------------------------------------------------------
# State checks
# ---------------------------------------------------------------------------

def is_demo_mode() -> bool:
    """Returns True if Demo Mode is currently active."""
    return st.session_state.get("demo_mode", False)


# ---------------------------------------------------------------------------
# Activation / deactivation
# ---------------------------------------------------------------------------

def activate_demo_mode():
    """Populates session state with demo data and restarts the app loop."""
    st.session_state.demo_mode = True
    st.session_state.candidate_profile = DEMO_CANDIDATE
    st.session_state.jobs = DEMO_JOBS_LIST
    st.session_state.selected_jobs = [DEMO_JOB]
    st.session_state.demo_jobs_fetched = True
    st.rerun()


def deactivate_demo_mode():
    """Clears all demo data and returns the app to its default state."""
    st.session_state.demo_mode = False
    st.session_state.jobs = []
    st.session_state.selected_jobs = []
    st.session_state.candidate_profile = {}
    st.session_state.results = {}
    st.session_state.demo_jobs_fetched = False
    st.rerun()


# ---------------------------------------------------------------------------
# Simulated pipeline
# ---------------------------------------------------------------------------

def run_demo_pipeline(status_container) -> dict:
    """
    Simulates the four-agent CrewAI pipeline with realistic timing.
    Writes progress steps to status_container and stores results in session state.

    Returns the DEMO_RESULTS dictionary.
    """
    with status_container:
        st.write("Job Analyzer Agent is analyzing the position...")
        time.sleep(2)
        st.write("Job requirements extracted successfully.")
        time.sleep(1)
        st.write("Resume Customizer Agent is tailoring your materials...")
        time.sleep(3)
        st.write("Resume summary and cover letter generated.")
        time.sleep(1)
        st.write("Messaging Agent is drafting your LinkedIn outreach...")
        time.sleep(2)
        st.write("LinkedIn message and follow-up drafted.")
        time.sleep(1)
        st.write("Interview Prep Agent is building your interview guide...")
        time.sleep(2)
        st.write("Interview preparation guide ready.")
        time.sleep(1)

    st.session_state.results[DEMO_JOB["job_id"]] = DEMO_RESULTS
    return DEMO_RESULTS


# ---------------------------------------------------------------------------
# UI helper
# ---------------------------------------------------------------------------

def get_demo_banner_html() -> str:
    """
    Returns the demo mode notice as a plain string.
    Callers should pass this to st.warning() — no custom HTML or CSS used.
    """
    return (
        "Demo Mode — You are viewing pre-generated sample outputs. "
        "Add your API key in the sidebar to run the real pipeline."
    )
