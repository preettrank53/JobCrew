import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.header("Your Profile")
        
        if st.session_state.get("candidate_profile"):
            st.success("Profile Ready")
            
        with st.form(key="candidate_form"):
            name = st.text_input("Name")
            experience = st.text_area("Work Experience", placeholder="e.g. - Data Analyst at TechCorp (3 years)\n- Built data pipelines and dashboards...")
            skills = st.text_area("Key Skills", placeholder="e.g. Python, SQL, Tableau, Communication...")
            education = st.text_input("Education Background", placeholder="e.g. B.S. in Computer Science")
            
            submit_button = st.form_submit_button("Save Profile")
            
            if submit_button:
                if not name.strip():
                    st.warning("Please provide your Name.")
                elif not experience.strip():
                    st.warning("Please provide your Work Experience.")
                elif not skills.strip():
                    st.warning("Please provide your Key Skills.")
                elif not education.strip():
                    st.warning("Please provide your Education Background.")
                else:
                    st.session_state.candidate_profile = {
                        "name": name,
                        "experience": experience,
                        "skills": [s.strip() for s in skills.split(',')] if skills else [],
                        "education": education
                    }
                    st.success("Profile saved successfully!")
                
        with st.expander("View Saved Profile"):
            if st.session_state.get("candidate_profile"):
                st.json(st.session_state.candidate_profile)
            else:
                st.info("No profile saved yet.")
                
        if st.button("Clear Profile"):
            st.session_state.candidate_profile = {}
            st.rerun()
