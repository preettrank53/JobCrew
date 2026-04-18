import sys
import os
import re

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew import run_jobcrew_pipeline

TEST_JOB_SAMPLES = [
    {
        "title": "Data Analyst",
        "department": "Department of Labor",
        "location": "Washington, DC",
        "salary_min": "89,000",
        "salary_max": "115,000",
        "close_date": "2026-12-31",
        "job_id": "DOL-12345",
        "apply_url": "https://usajobs.gov/job/12345",
        "description": "The Department of Labor is seeking a Data Analyst (GS-12) to join our strategic planning division. You will be responsible for developing statistical models, creating Tableau dashboards, and automating data pipelines using Python and SQL. Must have strong communication skills to present findings to senior leadership. Requires at least 4 years of experience in data modeling and a Bachelor's degree in a related field. Preference for candidates with active security clearance."
    },
    {
        "title": "Software Developer",
        "department": "Department of Veterans Affairs",
        "location": "Remote",
        "salary_min": "65,000",
        "salary_max": "85,000",
        "close_date": "2026-11-30",
        "job_id": "VA-54321",
        "apply_url": "https://usajobs.gov/job/54321",
        "description": "The VA is looking for a GS-9 Software Developer. Duties include maintaining web applications using React and Node.js, writing unit tests, and participating in Agile sprints. Minimum of 2 years experience with JavaScript and REST APIs is required. Familiarity with AWS and Docker is highly preferred. The ideal candidate will be mission-driven and dedicated to improving veterans' access to healthcare services."
    },
    {
        "title": "Program Analyst",
        "department": "Department of Homeland Security",
        "location": "Arlington, VA",
        "salary_min": "78,000",
        "salary_max": "101,000",
        "close_date": "2026-10-15",
        "job_id": "DHS-98765",
        "apply_url": "https://usajobs.gov/job/98765",
        "description": "DHS requires a Program Analyst (GS-11) to oversee budget formulation and track project milestones. The candidate will analyze financial data, prepare weekly briefing reports, and coordinate across multiple agencies. Requires 3 years of program management experience and strong proficiency in Excel and SharePoint. PMP certification is preferred but not mandatory. Must thrive in a fast-paced environment."
    }
]

TEST_CANDIDATE_PROFILE = {
    "name": "Jane Smith",
    "experience": "- Software Engineer at TechCorp (2022-2025): Developed React web apps, managed Node.js backend.\n- Data Analyst at DataSys (2019-2022): Built Python and SQL data pipelines, created Tableau dashboards.\n- Junior Analyst at Finance LLC (2017-2019): Managed Excel reporting and tracked budgets.",
    "skills": "Python, SQL, Tableau, React, Node.js, JavaScript, Data Modeling, Communication, AWS, Docker, Excel, SharePoint, Agile, Budget Formulation, Project Management",
    "education": "B.S. in Computer Science, University of Technology, 2017"
}

def score_job_analysis_output(output):
    headers = [
        "## POSITION OVERVIEW",
        "## MANDATORY REQUIREMENTS",
        "## PREFERRED QUALIFICATIONS",
        "## KEY RESPONSIBILITIES",
        "## CRITICAL KEYWORDS",
        "## CULTURE & ENVIRONMENT SIGNALS",
        "## APPLICATION STRATEGY"
    ]
    
    missing = []
    for header in headers:
        if header not in output:
            missing.append(header)
            
    score = len(headers) - len(missing)
    passed = score >= 5
    return {"score": score, "max_score": 7, "missing_sections": missing, "passed": passed}

def score_resume_output(output):
    headers = [
        "## TAILORED RESUME SUMMARY",
        "## KEY QUALIFICATIONS SECTION",
        "## COVER LETTER",
        "## ATS KEYWORD CHECKLIST"
    ]
    
    missing = []
    for header in headers:
        if header not in output:
            missing.append(header)
            
    # Check cover letter paragraphs
    try:
        if "## COVER LETTER" in output:
            start_idx = output.find("## COVER LETTER") + len("## COVER LETTER")
            end_idx = output.find("##", start_idx)
            if end_idx == -1: end_idx = len(output)
            
            cl_text = output[start_idx:end_idx].strip()
            paragraphs = [p for p in cl_text.split('\n\n') if p.strip()]
            if len(paragraphs) < 4:
                missing.append("COVER LETTER < 4 paragraphs")
    except Exception:
        missing.append("COVER LETTER paragraph check failed")

    # Check resume summary sentences
    try:
        if "## TAILORED RESUME SUMMARY" in output:
            start_idx = output.find("## TAILORED RESUME SUMMARY") + len("## TAILORED RESUME SUMMARY")
            end_idx = output.find("##", start_idx)
            if end_idx == -1: end_idx = len(output)
            
            summary_text = output[start_idx:end_idx].strip()
            sentences = [s for s in summary_text.split('.') if s.strip()]
            if not (3 <= len(sentences) <= 6):
                missing.append("RESUME SUMMARY not 3-6 sentences")
    except Exception:
        missing.append("RESUME SUMMARY sentence check failed")

    score = 6 - len(missing)
    if score < 0: score = 0
    passed = score >= 4
    return {"score": score, "max_score": 6, "missing_sections": missing, "passed": passed}

def score_messaging_output(output):
    headers = [
        "## LINKEDIN MESSAGE",
        "## SUBJECT LINE",
        "## FOLLOW-UP MESSAGE"
    ]
    
    missing = []
    for header in headers:
        if header not in output:
            missing.append(header)
            
    # Check linkedin message length
    try:
        if "## LINKEDIN MESSAGE" in output and "## SUBJECT LINE" in output:
            start_idx = output.find("## LINKEDIN MESSAGE") + len("## LINKEDIN MESSAGE")
            end_idx = output.find("## SUBJECT LINE")
            msg_text = output[start_idx:end_idx].strip()
            word_count = len(msg_text.split())
            if word_count > 300:
                missing.append("LINKEDIN MESSAGE > 300 words")
    except Exception:
        missing.append("LINKEDIN MESSAGE word count check failed")
        
    # Check subject line length
    try:
        if "## SUBJECT LINE" in output:
            start_idx = output.find("## SUBJECT LINE") + len("## SUBJECT LINE")
            end_idx = output.find("##", start_idx)
            if end_idx == -1: end_idx = len(output)
            sub_text = output[start_idx:end_idx].strip()
            if len(sub_text) > 200:
                missing.append("SUBJECT LINE > 200 characters")
    except Exception:
        missing.append("SUBJECT LINE length check failed")

    score = 5 - len(missing)
    if score < 0: score = 0
    passed = score >= 3
    return {"score": score, "max_score": 5, "missing_sections": missing, "passed": passed}

def run_quality_tests():
    total_passed = 0
    
    for idx, job in enumerate(TEST_JOB_SAMPLES):
        print(f"\n{'='*50}")
        print(f"TESTING JOB {idx+1}: {job['title']} at {job['department']}")
        print(f"{'='*50}")
        
        try:
            results = run_jobcrew_pipeline(job, TEST_CANDIDATE_PROFILE)
            
            ja_score = score_job_analysis_output(results.get("job_analysis", ""))
            res_score = score_resume_output(results.get("resume_and_cover_letter", ""))
            msg_score = score_messaging_output(results.get("linkedin_message", ""))
            
            job_passed = ja_score['passed'] and res_score['passed'] and msg_score['passed']
            if job_passed:
                total_passed += 1
                
            print(f"Job Analyzer: {ja_score['score']}/{ja_score['max_score']} [{'PASS' if ja_score['passed'] else 'FAIL'}]")
            if ja_score['missing_sections']: print(f"  Failed checks: {ja_score['missing_sections']}")
            
            print(f"Resume Customizer: {res_score['score']}/{res_score['max_score']} [{'PASS' if res_score['passed'] else 'FAIL'}]")
            if res_score['missing_sections']: print(f"  Failed checks: {res_score['missing_sections']}")
            
            print(f"Messaging Agent: {msg_score['score']}/{msg_score['max_score']} [{'PASS' if msg_score['passed'] else 'FAIL'}]")
            if msg_score['missing_sections']: print(f"  Failed checks: {msg_score['missing_sections']}")
            
            print(f"OVERALL JOB {idx+1} STATUS: {'PASS' if job_passed else 'FAIL'}")
            
        except Exception as e:
            print(f"Error running pipeline for Job {idx+1}: {e}")

    print(f"\n{'='*50}")
    print(f"TEST SUMMARY: {total_passed}/3 Jobs Passed")
    print(f"{'='*50}")

if __name__ == "__main__":
    run_quality_tests()
