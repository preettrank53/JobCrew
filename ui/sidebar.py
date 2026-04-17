import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("Your Profile")
        
        with st.form(key="candidate_form"):
            name = st.text_input("Name")
            experience = st.text_area("Work Experience", placeholder="e.g. - Data Analyst at TechCorp (3 years)\n- Built data pipelines and dashboards...")
            skills = st.text_area("Key Skills", placeholder="e.g. Python, SQL, Tableau, Communication...")
            education = st.text_input("Education Background", placeholder="e.g. B.S. in Computer Science")
            
            submit_button = st.form_submit_button("Save Profile")
            
            if submit_button:
                st.session_state.candidate_profile = {
                    "name": name,
                    "experience": experience,
                    "skills": [s.strip() for s in skills.split(',')] if skills else [],
                    "education": education
                }
                st.success("Profile saved successfully!")
                
        with st.expander("View Saved Profile"):
            if st.session_state.candidate_profile:
                st.json(st.session_state.candidate_profile)
            else:
                st.info("No profile saved yet.")
