import streamlit as st
from tracker.log_reader import get_tracker_summary, get_all_applications, get_application_by_id, delete_application_log
from tracker.status_manager import get_status_statistics, get_status_label, get_status, save_status, APPLICATION_STATUSES
from tools.output_formatter import format_output_for_display

def render_status_editor(log_id, job_title):
    current_status = get_status(log_id)
    current_key = current_status.get("status_key", "not_applied")
    current_notes = current_status.get("notes", "")
    
    options = list(APPLICATION_STATUSES.keys())
    labels = [APPLICATION_STATUSES[k]["label"] for k in options]
    current_index = options.index(current_key) if current_key in options else 0
    
    with st.container():
        st.markdown(f"**Edit Status:** {job_title}")
        with st.form(key=f"status_form_{log_id}"):
            selected_label = st.selectbox("Status", options=labels, index=current_index)
            notes = st.text_area("Notes", value=current_notes)
            
            submitted = st.form_submit_button("Save Status")
            if submitted:
                selected_key = options[labels.index(selected_label)]
                save_status(log_id, selected_key, notes)
                st.session_state.editing_status = None
                st.success("Status saved!")
                st.rerun()
                
        if st.button("Cancel", key=f"cancel_status_{log_id}"):
            st.session_state.editing_status = None
            st.rerun()

def render_tracker_dashboard():
    st.header("Application Tracker")
    
    summary = get_tracker_summary()
    total_apps = summary.get("total_applications", 0)
    
    # Split metrics into two rows to prevent text truncation
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Applications", total_apps)
    with col2:
        st.metric("Departments Targeted", len(summary.get("unique_departments", [])))
    with col3:
        most_recent = summary.get("most_recent", "")
        if most_recent and len(most_recent) >= 10:
            most_recent = most_recent[:10]
        else:
            most_recent = "N/A"
        st.metric("Most Recent", most_recent)
    with col4:
        st.metric("Storage Used", f"{summary.get('total_size_kb', 0)} KB")
        
    status_stats = get_status_statistics()
    st.write("") # small spacing
    m_col1, m_col2, m_col3, _ = st.columns([1, 1, 1, 1])
    with m_col1:
        st.metric("Applied", status_stats.get("applied", 0))
    with m_col2:
        st.metric("Interviewing", status_stats.get("interviewing", 0))
    with m_col3:
        st.metric("Offers", status_stats.get("offer_received", 0))
        
    if total_apps == 0:
        st.info("No applications tracked yet — run the pipeline to generate your first application materials")
        return
        
    st.divider()
    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([3, 2, 2, 2])
    
    with filter_col1:
        search_term = st.text_input("Search by job title or department", key="tracker_search")
    
    with filter_col2:
        dept_options = ["All Departments"] + summary.get("unique_departments", [])
        selected_dept = st.selectbox("Filter by Department", options=dept_options)
        
    with filter_col3:
        status_options = ["All Statuses"] + [v["label"] for v in APPLICATION_STATUSES.values()]
        selected_status_label = st.selectbox("Filter by Status", options=status_options)
        
    with filter_col4:
        sort_by = st.selectbox("Sort By", options=["Newest First", "Oldest First", "Job Title A-Z", "Department A-Z"])
        
    apps = get_all_applications()
    
    if search_term:
        search_term = search_term.lower()
        apps = [a for a in apps if search_term in a.get("job_title", "").lower() or search_term in a.get("department", "").lower()]
        
    if selected_dept != "All Departments":
        apps = [a for a in apps if a.get("department", "") == selected_dept]
        
    if selected_status_label != "All Statuses":
        selected_status_key = next(k for k, v in APPLICATION_STATUSES.items() if v["label"] == selected_status_label)
        apps = [a for a in apps if get_status(a.get("log_id")).get("status_key", "not_applied") == selected_status_key]
        
    if sort_by == "Newest First":
        apps.sort(key=lambda x: x.get("generated_at", ""), reverse=True)
    elif sort_by == "Oldest First":
        apps.sort(key=lambda x: x.get("generated_at", ""))
    elif sort_by == "Job Title A-Z":
        apps.sort(key=lambda x: x.get("job_title", ""))
    elif sort_by == "Department A-Z":
        apps.sort(key=lambda x: x.get("department", ""))
        
    st.subheader("Tracked Applications")
    for app in apps:
        log_id = app.get("log_id")
        current_status = get_status(log_id)
        current_status_key = current_status.get("status_key", "not_applied")
        status_label_text = get_status_label(log_id)
        
        color = "grey"
        if current_status_key in ["applied", "offer_received"]: color = "green"
        elif current_status_key == "interviewing": color = "blue"
        elif current_status_key in ["rejected", "withdrawn"]: color = "red"
        
        with st.container():
            # Adjust columns to 60/40 ratio to give buttons more breathing room
            col_info, col_actions = st.columns([6, 4])
            with col_info:
                st.markdown(f"**{app.get('job_title', 'Unknown Title')}**")
                st.caption(f"{app.get('department', 'Unknown Department')} | Generated: {app.get('generated_at', 'Unknown Date')}")
                st.markdown(f"<span style='color:{color}; font-weight:bold;'>{status_label_text}</span>", unsafe_allow_html=True)
                
            with col_actions:
                st.write("") # slight alignment nudge
                act1, act2, act3 = st.columns(3)
                with act1:
                    if st.button("View", key=f"view_{log_id}", use_container_width=True):
                        st.session_state.viewing_application = log_id
                        st.rerun()
                with act2:
                    if st.button("Status", key=f"status_{log_id}", use_container_width=True):
                        if st.session_state.get('editing_status') == log_id:
                            st.session_state.editing_status = None
                        else:
                            st.session_state.editing_status = log_id
                        st.rerun()
                with act3:
                    if st.button("Delete", key=f"delete_{log_id}", use_container_width=True):
                        delete_application_log(log_id)
                        st.success("Application deleted successfully.")
                        if st.session_state.get('viewing_application') == log_id:
                            st.session_state.viewing_application = None
                        if st.session_state.get('editing_status') == log_id:
                            st.session_state.editing_status = None
                        st.rerun()
                        
            if st.session_state.get('editing_status') == log_id:
                render_status_editor(log_id, app.get('job_title', 'Unknown'))
                
            st.divider()
            
    if st.session_state.get('viewing_application'):
        try:
            detail_app = get_application_by_id(st.session_state.viewing_application)
            with st.expander(f"Viewing: {detail_app.get('job_title')} — {detail_app.get('department')}", expanded=True):
                st.markdown(f"**Candidate:** {detail_app.get('candidate_name')} | **Generated:** {detail_app.get('generated_at')} | **Job ID:** {detail_app.get('job_id')} | **Size:** {detail_app.get('file_size_kb')} KB")
                
                tab1, tab2, tab3 = st.tabs(["Job Analysis", "Resume & Cover Letter", "LinkedIn Message"])
                with tab1:
                    st.markdown(format_output_for_display(detail_app.get('job_analysis', ''), 'analysis'))
                with tab2:
                    st.markdown(format_output_for_display(detail_app.get('resume_and_cover_letter', ''), 'resume'))
                with tab3:
                    st.markdown(format_output_for_display(detail_app.get('linkedin_message', ''), 'messaging'))
                
                with open(detail_app['file_path'], 'r', encoding='utf-8') as f:
                    file_content = f.read()
                    
                st.download_button("Download Application Materials", data=file_content, file_name=f"jobcrew_export_{detail_app['log_id']}.txt")
                
                if st.button("Close Detail View"):
                    st.session_state.viewing_application = None
                    st.rerun()
        except FileNotFoundError:
            st.error("Log file not found.")
            st.session_state.viewing_application = None
