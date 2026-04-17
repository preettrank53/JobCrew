import streamlit as st
from ui.layout import set_page_config, render_header, initialize_session_state
from ui.sidebar import render_sidebar
from ui.job_search import render_job_search_panel
from ui.pipeline_runner import render_pipeline_runner

def main():
    set_page_config()
    initialize_session_state()
    render_header()
    render_sidebar()
    render_job_search_panel()
    st.divider()
    render_pipeline_runner()

if __name__ == "__main__":
    main()
