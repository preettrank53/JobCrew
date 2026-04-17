import streamlit as st
import datetime

def inject_custom_css():
    st.markdown("""
        <style>
            /* Custom CSS removed to support Streamlit native Dark Mode */
        </style>
    """, unsafe_allow_html=True)

def render_metric_bar(jobs_fetched, jobs_selected, materials_generated):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Jobs Fetched", jobs_fetched)
    with col2:
        st.metric("Positions Selected", jobs_selected)
    with col3:
        st.metric("Materials Generated", materials_generated)

def render_footer():
    st.divider()
    year = datetime.datetime.now().year
    # Updated text to reflect Ollama implementation while keeping the exact styling requested
    st.markdown(
        f"<p style='text-align: center; color: gray; font-size: 0.9em;'>"
        f"Built with ❤️ using CrewAI · LangChain · Ollama · Streamlit © {year}"
        f"</p>",
        unsafe_allow_html=True
    )
