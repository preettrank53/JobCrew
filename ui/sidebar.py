import streamlit as st
from tools.profile_extractor import get_cached_profile_extraction
from tools.resume_parser import parse_resume_file


PROVIDER_GROQ = "Groq (Free & Fast - Recommended)"
PROVIDER_GEMINI = "Google Gemini"
PROVIDER_OPENAI = "OpenAI"

PROVIDER_OPTIONS = [PROVIDER_GROQ, PROVIDER_GEMINI, PROVIDER_OPENAI]

PROVIDER_KEY_LABELS = {
    PROVIDER_GROQ:   ("Groq API Key",   "Get a free key at console.groq.com"),
    PROVIDER_GEMINI: ("Gemini API Key", "Get a key at aistudio.google.com"),
    PROVIDER_OPENAI: ("OpenAI API Key", "Get a key at platform.openai.com"),
}


def render_api_key_section():
    """Renders the LLM API key configuration section at the top of the sidebar."""
    st.sidebar.header("API Configuration")

    key_saved = bool(st.session_state.get("user_llm_key", "").strip())
    provider_saved = st.session_state.get("llm_provider", PROVIDER_GROQ)

    if key_saved:
        st.sidebar.success(f"LLM Key Configured ({provider_saved})")

    with st.sidebar.expander("Configure your LLM API Key", expanded=not key_saved):
        provider = st.radio(
            "Select your AI provider:",
            options=PROVIDER_OPTIONS,
            index=PROVIDER_OPTIONS.index(provider_saved),
            key="llm_provider_radio"
        )
        st.session_state.llm_provider = provider

        label, help_text = PROVIDER_KEY_LABELS[provider]
        api_key = st.text_input(
            label,
            type="password",
            help=help_text,
            value=st.session_state.get("user_llm_key", ""),
            key="llm_key_input"
        )

        if provider == PROVIDER_GROQ:
            st.caption("Groq is completely free - [Get key](https://console.groq.com)")

        if st.button("Save API Key", key="save_api_key_btn"):
            if not api_key.strip():
                st.error("API key cannot be empty.")
            elif len(api_key.strip()) < 20:
                st.error("API key appears too short. Please verify you copied the full key.")
            else:
                st.session_state.user_llm_key = api_key.strip()
                st.session_state.llm_provider = provider
                st.success("API Key saved - pipeline is ready")
                st.rerun()

    st.sidebar.divider()


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
                st.success("Profile auto-filled from resume. Review and edit below if needed.")
                st.rerun()
            except ValueError as ve:
                st.error(str(ve))
            except Exception:
                st.error("Unexpected error during profile extraction - please try manual entry")


def render_sidebar():
    with st.sidebar:
        render_api_key_section()

        st.header("Your Profile")

        input_mode = st.radio(
            "How would you like to set up your profile?",
            options=["Upload Resume (Auto-fill)", "Fill Manually"]
        )
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
            experience = st.text_area(
                "Work Experience",
                value=exp_val,
                placeholder="e.g. - Data Analyst at TechCorp (3 years)\n- Built data pipelines..."
            )
            skills = st.text_area(
                "Key Skills",
                value=skills_val,
                placeholder="e.g. Python, SQL, Tableau, Communication..."
            )
            education = st.text_input(
                "Education Background",
                value=edu_val,
                placeholder="e.g. B.S. in Computer Science"
            )

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
                        "skills": [s.strip() for s in skills.split(",") if s.strip()],
                        "education": education
                    }
                    st.success("Profile saved successfully.")

        with st.expander("View Saved Profile"):
            if st.session_state.get("candidate_profile"):
                st.json(st.session_state.candidate_profile)
            else:
                st.info("No profile saved yet.")

        if st.button("Clear Profile"):
            st.session_state.candidate_profile = {}
            st.rerun()
