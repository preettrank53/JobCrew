import streamlit as st
from tools.profile_extractor import get_cached_profile_extraction
from tools.resume_parser import parse_resume_file

def render_resume_upload_section():
    uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "txt"], key="resume_uploader")
    st.caption("Supported formats: PDF, TXT - Max 5MB")
    
    if st.button("Auto-fill Profile from Resume", key="autofill_btn"):
        if not uploaded_file:
            st.warning("Please upload a file first.")
            return
            
        with st.spinner("Reading resume and extracting profile with AI..."):
            try:
                resume_text = parse_resume_file(uploaded_file)
                profile = get_cached_profile_extraction(resume_text)
                st.session_state.candidate_profile = profile
                st.success("Profile auto-filled from resume! Review and edit below if needed.")
                st.rerun()
            except ValueError as ve:
                st.error(str(ve))
            except Exception:
                st.error("Unexpected error during profile extraction - please try manual entry")

def render_sidebar():
    with st.sidebar:
        st.header("Your Profile")
        
        input_mode = st.radio("How would you like to set up your profile?", options=["Upload Resume (Auto-fill)", "Fill Manually"])
        st.divider()
        
        if st.session_state.get("candidate_profile"):
            st.success("Profile Ready")
            
        if input_mode == "Upload Resume (Auto-fill)":
            render_resume_upload_section()
            
        with st.form(key="candidate_form"):
            profile = st.session_state.get("candidate_profile", {})
            
            exp_val = profile.get("experience", "")
            if isinstance(exp_val, list):
                exp_val = "\n".join([str(item) for item in exp_val])
                
            skills_val = profile.get("skills", "")
            if isinstance(skills_val, list):
                skills_val = ", ".join([str(item) for item in skills_val])
                
            edu_val = profile.get("education", "")
            if isinstance(edu_val, list):
                edu_val = "\n".join([str(item) for item in edu_val])
            
            name = st.text_input("Name", value=profile.get("name", ""))
            experience = st.text_area("Work Experience", value=exp_val, placeholder="e.g. - Data Analyst at TechCorp (3 years)\n- Built data pipelines and dashboards...")
            skills = st.text_area("Key Skills", value=skills_val, placeholder="e.g. Python, SQL, Tableau, Communication...")
            education = st.text_input("Education Background", value=edu_val, placeholder="e.g. B.S. in Computer Science")
            
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
