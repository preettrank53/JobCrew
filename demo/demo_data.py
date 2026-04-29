"""
Pre-cached realistic demo data for JobCrew Demo Mode.
All content is fictional and used solely for demonstration purposes.
"""

# ---------------------------------------------------------------------------
# Demo Job (primary position used by the pipeline demo)
# ---------------------------------------------------------------------------

DEMO_JOB = {
    "job_id": "DEMO-VA-DS-GS12-2024",
    "title": "Data Scientist (Healthcare Analytics)",
    "department": "Department of Veterans Affairs",
    "location": "Washington, DC (Hybrid)",
    "salary_min": "89835",
    "salary_max": "116788",
    "close_date": "2024-12-31",
    "apply_url": "https://www.usajobs.gov/",
    "description": (
        "The Department of Veterans Affairs, Office of Analytics and Performance Integration, "
        "is seeking a Data Scientist to support veteran healthcare analytics initiatives. "
        "The incumbent will design, develop, and maintain end-to-end data pipelines using Python "
        "and SQL, build and deploy machine learning models to improve clinical decision support, "
        "and translate complex analytical findings into actionable insights for senior leadership. "
        "This position requires experience with large-scale healthcare datasets, federal data "
        "governance standards, and cloud-based data infrastructure. The successful candidate will "
        "collaborate closely with clinical informatics teams, IT architects, and program officers "
        "to accelerate the VA's data-driven transformation in veteran health outcomes research."
    ),
}

# ---------------------------------------------------------------------------
# Demo Candidate Profile
# ---------------------------------------------------------------------------

DEMO_CANDIDATE = {
    "name": "Alex Johnson",
    "experience": (
        "- Senior Data Analyst, Centers for Disease Control and Prevention (CDC) | 3 years\n"
        "  Developed automated ETL pipelines in Python processing 50M+ health records weekly. "
        "Led cross-functional team of 6 analysts to deliver a predictive sepsis risk model "
        "achieving 87% sensitivity in clinical trials.\n\n"
        "- Data Scientist, Booz Allen Hamilton | 2 years\n"
        "  Designed NLP pipelines for federal client text analytics projects. Built and deployed "
        "gradient-boosted classification models using scikit-learn and XGBoost on AWS SageMaker. "
        "Delivered dashboards in Tableau and Power BI consumed by 200+ stakeholders.\n\n"
        "- Business Intelligence Analyst, MITRE Corporation | 2 years\n"
        "  Maintained SQL data warehouse serving 15 internal teams. Created KPI reporting "
        "infrastructure and automated monthly executive briefing packages using Python and "
        "Pandas, reducing manual effort by 40%."
    ),
    "skills": (
        "Python, SQL, Machine Learning, scikit-learn, XGBoost, TensorFlow, Pandas, NumPy, "
        "Tableau, Power BI, AWS SageMaker, ETL Pipeline Development, Data Governance, "
        "NLP, Statistical Modeling, Federal Compliance, Git, Agile, Data Visualization, "
        "Healthcare Analytics"
    ),
    "education": "M.S. in Data Science, Georgetown University, 2019",
}

# ---------------------------------------------------------------------------
# Demo Pipeline Results
# ---------------------------------------------------------------------------

DEMO_RESULTS = {
    "job_title": "Data Scientist (Healthcare Analytics)",
    "department": "Department of Veterans Affairs",
    "execution_time_seconds": 47.3,

    "job_analysis": """\
## POSITION OVERVIEW
**Title:** Data Scientist (Healthcare Analytics) — GS-12
**Agency:** Department of Veterans Affairs, Office of Analytics and Performance Integration
**Location:** Washington, DC (Hybrid)
**Salary:** $89,835 — $116,788 per annum
**Closing Date:** December 31, 2024

## MANDATORY REQUIREMENTS
- U.S. Citizenship required for federal employment eligibility
- Minimum 3 years of professional data science experience with demonstrated Python proficiency
- Hands-on experience designing and maintaining production-grade data pipelines
- Proven track record building and deploying supervised machine learning models
- Experience working with large-scale structured and semi-structured datasets (10M+ records)

## PREFERRED QUALIFICATIONS
- Prior experience with healthcare or clinical datasets and HIPAA compliance frameworks
- Familiarity with federal data governance standards (NIST, FedRAMP) and VA-specific systems
- Cloud platform certification (AWS, Azure, or GCP) with SageMaker or equivalent MLOps tools
- Graduate degree (M.S. or Ph.D.) in Data Science, Statistics, Computer Science, or related field

## KEY RESPONSIBILITIES
- Design, build, and maintain automated ETL and data pipeline infrastructure using Python and SQL
- Develop predictive and prescriptive ML models to improve clinical decision support for veteran healthcare
- Translate analytical findings into clear, actionable briefings for senior leadership and program officers
- Collaborate with clinical informatics teams and IT architects on data architecture decisions
- Ensure data quality, lineage, and governance compliance across all analytical outputs
- Maintain documentation of models, pipelines, and methodologies to federal standards

## CRITICAL KEYWORDS
data pipelines, Python, machine learning, healthcare analytics, SQL, veteran health outcomes,
scikit-learn, ETL, federal compliance, data governance

## CULTURE & ENVIRONMENT SIGNALS
- Mission-driven organization with a direct impact on veteran health and well-being
- Collaborative cross-functional environment spanning clinical, technical, and policy domains
- Strong emphasis on data quality, audit trails, and federally compliant analytical practices

## APPLICATION STRATEGY
Lead your application materials with direct evidence of healthcare or mission-critical data work —
the VA will prioritize candidates who can demonstrate domain familiarity alongside technical depth.
Quantify all pipeline scale and model performance metrics explicitly; federal reviewers rely on
numbers to score applications against OPM qualification standards. Mirror the exact language from
the posting (data pipelines, veteran healthcare analytics, machine learning) throughout your resume
to maximize ATS scoring before human review.
""",

    "resume_and_cover_letter": """\
## TAILORED RESUME SUMMARY
Results-driven Data Scientist with 7 years of federal and government-adjacent analytics experience,
specializing in end-to-end ML pipeline development, clinical healthcare datasets, and data
governance at scale. Proven track record delivering predictive models and ETL infrastructure that
directly supports mission-critical decision-making for federal health agencies. Seeking to leverage
deep expertise in Python, machine learning, and large-scale healthcare analytics to advance the
Department of Veterans Affairs' data-driven transformation of veteran health outcomes.

## KEY QUALIFICATIONS SECTION
- Designed and maintained Python-based ETL pipelines processing 50M+ CDC health records weekly,
  directly analogous to the VA's large-scale veteran healthcare data infrastructure needs
- Built and deployed gradient-boosted classification and predictive risk models (XGBoost, scikit-learn)
  achieving 87% sensitivity — demonstrating production-ready ML delivery for clinical contexts
- 5+ years of direct federal and federal-contractor experience (CDC, Booz Allen Hamilton, MITRE),
  ensuring full familiarity with federal compliance, data governance, and audit standards
- Delivered NLP text analytics pipelines on AWS SageMaker for federal clients, matching the VA's
  cloud-based data infrastructure mentioned in the position description
- Graduate degree (M.S., Data Science, Georgetown) satisfies the VA's preferred qualification for
  advanced education in a quantitative discipline
- Reduced executive reporting manual effort by 40% through Python automation — demonstrates the
  ability to translate analytical work into leadership-facing insights
- Cross-functional collaboration experience spanning clinical, technical, and policy stakeholders
  at organizations of comparable complexity to the VA's integrated environment

## COVER LETTER

Dear Hiring Manager,
Department of Veterans Affairs, Office of Analytics and Performance Integration

I am writing to express my strong interest in the Data Scientist (Healthcare Analytics) position
(Announcement DEMO-VA-DS-GS12-2024). With seven years of progressive data science experience
across federal agencies and government contractors — including the CDC and Booz Allen Hamilton —
I bring a combination of technical depth and mission-driven focus that aligns directly with the
VA's objectives in veteran healthcare analytics.

In my most recent role at the CDC, I led the design and operation of Python-based ETL pipelines
processing more than 50 million health records weekly, and I directed a cross-functional team that
delivered a predictive sepsis risk model with 87% clinical sensitivity. This experience maps
precisely to the core responsibilities outlined in your posting: building production-grade data
pipelines, developing machine learning models to improve clinical decision support, and
collaborating with clinical and technical stakeholders on data architecture. I am equally
comfortable writing complex SQL queries, managing cloud-based ML workflows on AWS SageMaker,
and translating results into executive briefings for senior leadership.

What draws me specifically to this opportunity is the VA's commitment to using data as a lever for
improving veteran health outcomes. Having spent my career supporting mission-critical federal health
programs, I understand both the technical rigor and the stakes involved. I am well-versed in
federal data governance standards, HIPAA compliance, and the documentation requirements that
distinguish high-quality analytical work in a government context.

I would welcome the opportunity to discuss how my background in healthcare data pipelines,
predictive modeling, and federal compliance can contribute to the VA's data-driven mission.
Thank you for your time and consideration.

Sincerely,
Alex Johnson

## ATS KEYWORD CHECKLIST
- data pipelines: Present
- Python: Present
- machine learning: Present
- healthcare analytics: Present
- SQL: Present
- ETL: Present
- scikit-learn: Present
- data governance: Present
- federal compliance: Present
- veteran health outcomes: Present
""",

    "linkedin_message": """\
## LINKEDIN MESSAGE
Subject: Data Scientist Role — Department of Veterans Affairs

Dear [Recruiter/Hiring Manager Name],

I came across the Data Scientist (Healthcare Analytics) opening at the Department of Veterans
Affairs and wanted to reach out directly. I have spent the last seven years building data
pipelines and machine learning models for federal health agencies, including three years at the
CDC where my team delivered a predictive clinical risk model now used across 12 regional
health centers.

The VA's focus on using data to improve veteran health outcomes strongly resonates with me —
it is the kind of mission I have been working toward throughout my career. I am particularly
drawn to the cross-functional nature of this role, bridging clinical informatics, IT
architecture, and senior leadership, which mirrors the environments where I have done my most
impactful work.

I noticed your background in federal health informatics, and I believe you would be able to
speak to the culture and expectations within the Office of Analytics and Performance
Integration. I would be grateful for 15 minutes of your time to learn more about the team and
share how my experience translates to this position.

Thank you for your consideration.

Best regards,
Alex Johnson

## SUBJECT LINE
Federal Data Scientist with CDC healthcare pipeline experience — interested in VA GS-12 opening

## FOLLOW-UP MESSAGE
Dear [Name],

I wanted to follow up on the message I sent last week regarding the Data Scientist role at the
Department of Veterans Affairs. I remain genuinely interested in the position and the VA's
healthcare analytics mission. If you have had a chance to review my background, I would welcome
a brief conversation at your convenience. I am happy to share specific examples of my federal
pipeline and ML work. Thank you again for your time.

Best regards,
Alex Johnson
""",

    "interview_prep": """\
## INTERVIEW PREPARATION REPORT

## TECHNICAL QUESTIONS (3)

### Question 1: How do you approach designing and maintaining production-grade data pipelines, particularly for large-scale structured and semi-structured datasets?
**Why they ask this:** They need to verify your technical depth in ETL and your ability to handle 10M+ records.
**Your Answer Framework:** Leverage your experience at the CDC. Discuss the automated ETL pipelines you developed in Python that processed 50M+ health records weekly.
**Key Points to Hit:**
- Mention the scale (50M+ records weekly).
- Highlight the use of Python for automation.
- Connect this to the VA's need for end-to-end data pipelines in healthcare analytics.

### Question 2: Can you walk us through a supervised machine learning model you built and deployed, and how it improved clinical decision support?
**Why they ask this:** They want to see your track record of deploying ML models that have a tangible impact.
**Your Answer Framework:** Talk about the predictive sepsis risk model you delivered at the CDC.
**Key Points to Hit:**
- Describe the model and its purpose (predictive sepsis risk).
- Mention the sensitivity achieved (87% in clinical trials).
- Relate this to their goal of improving clinical decision support for veterans.

### Question 3: Describe your experience working with federal data governance standards and how you ensure compliance in your analytical outputs.
**Why they ask this:** Federal compliance (NIST, FedRAMP, HIPAA) is a preferred qualification and crucial for handling veteran data.
**Your Answer Framework:** Draw from your 5+ years of federal experience, especially at Booz Allen Hamilton and MITRE.
**Key Points to Hit:**
- Emphasize your familiarity with federal client projects.
- Mention specific practices you use to ensure data quality, lineage, and audit trails.
- Confirm your understanding of the importance of compliance in mission-critical environments.

## BEHAVIORAL QUESTIONS (3)

### Question 4: Tell me about a time you had to translate complex analytical findings into actionable insights for senior leadership.
**Why they ask this:** A key responsibility is presenting findings to program officers and leadership who may not be technical.
**STAR Framework:**
- Situation: At MITRE Corporation, senior leadership needed clear visibility into performance metrics.
- Task: You were responsible for creating KPI reporting infrastructure for 15 internal teams.
- Action: You automated monthly executive briefing packages using Python and Pandas.
- Result: Reduced manual effort by 40% and successfully delivered actionable insights to leadership.

### Question 5: Give an example of a project where you had to collaborate closely with cross-functional teams, such as IT architects or clinical informatics teams.
**Why they ask this:** The role requires strong collaboration across clinical, technical, and policy domains.
**STAR Framework:**
- Situation: At the CDC, you led a cross-functional team of 6 analysts.
- Task: The team needed to deliver a predictive sepsis risk model.
- Action: You coordinated efforts across different specialties to ensure the model met clinical needs and technical standards.
- Result: Successfully delivered a model achieving 87% sensitivity in clinical trials.

### Question 6: Describe a situation where you had to maintain documentation of models, pipelines, and methodologies to meet strict standards.
**Why they ask this:** Federal standards require meticulous documentation of all analytical work.
**STAR Framework:**
- Situation: Working on NLP pipelines for federal client text analytics projects at Booz Allen Hamilton.
- Task: Ensuring all models deployed on AWS SageMaker were fully documented according to federal compliance standards.
- Action: You maintained comprehensive documentation of methodologies and data governance practices.
- Result: Delivered dashboards and models that were compliant and easily consumed by 200+ stakeholders.

## SITUATIONAL QUESTIONS (2)

### Question 7: Imagine you discover a significant data quality issue in a dataset you are using to build a predictive model for clinical decision support. How do you handle it?
**Why they ask this:** They want to know your approach to data integrity, which is a strong emphasis in their culture.
**Suggested Approach:** Emphasize transparency and rigor. Frame your answer around immediately halting the use of the flawed data, investigating the root cause, communicating the issue to the clinical informatics team, and establishing an audit trail for the correction process.

### Question 8: You are asked to prioritize multiple urgent analytical requests from different program officers. How do you decide what to tackle first?
**Why they ask this:** In a mission-driven, fast-paced environment, balancing competing priorities is essential.
**Suggested Approach:** Discuss prioritizing based on mission impact (veteran health and well-being) and strategic alignment. Mention consulting with senior leadership to ensure your focus aligns with the Office of Analytics and Performance Integration's immediate goals.

## ROLE-SPECIFIC QUESTIONS (2)

### Question 9: How would your experience with NLP text analytics at Booz Allen Hamilton translate to the VA's objective of accelerating data-driven transformation in veteran health outcomes research?
**Why they ask this:** They want to see if you can connect your specific past work to their current strategic goals.
**Key Points to Hit:**
- Explain how NLP can extract insights from unstructured clinical notes.
- Tie this back to improving clinical decision support.
- Express enthusiasm for applying these techniques to veteran health outcomes.

### Question 10: The role involves working with cloud-based data infrastructure. Can you elaborate on your experience with AWS SageMaker and how you would utilize it for our predictive ML models?
**Why they ask this:** Cloud platform certification and experience with tools like SageMaker are preferred qualifications.
**Key Points to Hit:**
- Detail your experience deploying gradient-boosted classification models on AWS SageMaker.
- Discuss how SageMaker facilitates model lifecycle management.
- Highlight your readiness to leverage their cloud infrastructure from day one.

## INTERVIEW STRATEGY SUMMARY
Your strongest advantage is your direct experience with large-scale healthcare data pipelines at the CDC and your proven ability to deliver predictive clinical models. Lean heavily on these specific examples. When answering questions, consistently frame your technical achievements in terms of their impact on the organization's mission, mirroring the VA's focus on veteran health outcomes. Demonstrate that you not only possess the required Python and ML skills but also fully grasp the importance of federal data governance and cross-functional collaboration in a clinical setting.
""",
}


# ---------------------------------------------------------------------------
# Demo Jobs List (three positions for the search results panel)
# ---------------------------------------------------------------------------

DEMO_JOBS_LIST = [
    DEMO_JOB,
    {
        "job_id": "DEMO-DOE-DE-GS11-2024",
        "title": "Data Engineer",
        "department": "Department of Energy",
        "location": "Remote",
        "salary_min": "73217",
        "salary_max": "95116",
        "close_date": "2024-11-30",
        "apply_url": "https://www.usajobs.gov/",
        "description": (
            "The Department of Energy seeks a Data Engineer to build and maintain scalable "
            "data infrastructure supporting clean energy research initiatives. Responsibilities "
            "include designing data models, building ingestion pipelines, and ensuring data "
            "quality across enterprise platforms. Experience with Python, Apache Spark, and "
            "cloud data warehouses required."
        ),
    },
    {
        "job_id": "DEMO-HHS-ML-GS13-2024",
        "title": "Machine Learning Engineer",
        "department": "Department of Health and Human Services",
        "location": "Rockville, MD (Hybrid)",
        "salary_min": "112015",
        "salary_max": "145617",
        "close_date": "2024-12-15",
        "apply_url": "https://www.usajobs.gov/",
        "description": (
            "HHS Office of the Chief Data Officer is hiring a Machine Learning Engineer to "
            "develop and operationalize ML models supporting public health surveillance and "
            "federal program evaluation. The role requires expertise in MLOps, model lifecycle "
            "management, Python, and cloud platforms. Experience with healthcare data, NLP, "
            "and federal security frameworks is strongly preferred."
        ),
    },
]

# ---------------------------------------------------------------------------
# Demo Profile Extracted (simulates resume auto-extraction result)
# ---------------------------------------------------------------------------

DEMO_PROFILE_EXTRACTED = DEMO_CANDIDATE.copy()
