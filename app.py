import streamlit as st
from ui.layout import set_page_config, render_header, initialize_session_state, render_workflow_guide
from ui.sidebar import render_sidebar
from ui.job_search import render_job_search_panel
from ui.pipeline_runner import render_pipeline_runner
from ui.styles import inject_custom_css, render_metric_bar, render_footer

set_page_config()

def main():
    inject_custom_css()
    initialize_session_state()
    render_sidebar()
    render_header()
    render_workflow_guide()
    
    jobs_fetched = len(st.session_state.get('jobs', []))
    jobs_selected = len(st.session_state.get('selected_jobs', []))
    materials_generated = len(st.session_state.get('results', {}))
    render_metric_bar(jobs_fetched, jobs_selected, materials_generated)
    
    st.divider()
    render_job_search_panel()
    st.divider()
    render_pipeline_runner()
    render_footer()

if __name__ == "__main__":
    main()
