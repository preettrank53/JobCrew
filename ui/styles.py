import streamlit as st
import datetime



def render_metric_bar(jobs_fetched, jobs_selected, materials_generated, demo_active=False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Jobs Fetched", jobs_fetched)
    with col2:
        st.metric("Positions Selected", jobs_selected)
    with col3:
        st.metric("Materials Generated", materials_generated)
    with col4:
        st.metric("Mode", "Demo" if demo_active else "Live")

def render_footer():
    st.divider()
    year = datetime.datetime.now().year
    # Updated text to reflect Ollama implementation while keeping the exact styling requested
    st.markdown(
        f"<p style='text-align: center; color: gray; font-size: 0.9em;'>"
        f"Built with ❤️ using CrewAI · LangChain · Groq · Streamlit © {year}"
        f"</p>",
        unsafe_allow_html=True
    )
