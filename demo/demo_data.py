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
    "execution_time_seconds": 62.1,

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
## LIKELY INTERVIEW QUESTIONS
1. Can you walk us through how you built a data pipeline and what tools you used?
2. Tell us about a machine learning model you built. How did you decide which algorithm to use?
3. Have you worked with healthcare or clinical data before? What challenges did you face?
4. How do you make sure your data is accurate and complete before using it for analysis?
5. Describe a time when you had to explain a complex data result to someone who is not technical.
6. How have you handled a situation where a model you built did not perform as expected?
7. Have you worked in a federal or government environment? How did you manage compliance requirements?
8. Tell us about a time you worked across different teams — like IT, clinical, and management — to deliver a project.

## SUGGESTED ANSWERS
1. Data pipeline question
   - Situation: At the CDC, the team was processing health records from multiple state systems that came in different formats.
   - Task: I needed to build a reliable pipeline that could handle 50 million records every week without errors.
   - Action: I used Python with Pandas and Apache Airflow to automate the ingestion, cleaning, and loading steps. I added error logging at each stage so failures were easy to find and fix.
   - Result: The pipeline ran every week without manual intervention. Data quality issues dropped by 60% in the first three months.

2. Machine learning model question
   - Situation: The CDC wanted a way to identify patients at high risk of sepsis early.
   - Task: I had to choose and build a model that clinical staff could actually trust and use.
   - Action: I tested three algorithms — logistic regression, random forest, and XGBoost. XGBoost performed best in cross-validation. I also used SHAP values to explain which features drove each prediction, so doctors could understand the output.
   - Result: The model reached 87% sensitivity and was deployed across 12 regional health centers.

3. Healthcare data question
   - Situation: At Booz Allen Hamilton, I worked on a federal health client project with patient records that had missing values and inconsistent coding.
   - Task: I needed to clean and standardize the data before any analysis could happen.
   - Action: I mapped all diagnosis codes to a standard format, imputed missing values using median substitution for numerical fields, and flagged records with too many gaps for manual review.
   - Result: The cleaned dataset reduced downstream errors in the analytics reports by 45%.

4. Data quality question
   - Situation: At MITRE, I found that some monthly reports had wrong numbers because source data was being updated after the extract was taken.
   - Task: I needed to set up a process to catch these issues before the data reached the reports.
   - Action: I built automated data quality checks in Python that compared record counts, checked for duplicate IDs, and validated value ranges against known limits. Any failure sent an alert before the pipeline completed.
   - Result: Report errors were eliminated. Stakeholder trust in the data improved noticeably.

5. Explaining complex results question
   - Situation: At the CDC, senior leadership needed to understand why the sepsis model was flagging certain patient groups at higher rates.
   - Task: I had to explain the model's findings without using technical language.
   - Action: I created a simple one-page summary with charts showing which factors mattered most, using plain words like "older patients with two or more existing conditions are flagged more often because past data shows higher risk."
   - Result: Leadership approved the model for wider rollout after that briefing. They said it was the clearest technical explanation they had received.

6. Model underperformance question
   - Situation: At Booz Allen, a text classification model I built was only getting 65% accuracy in production, even though it had 82% in testing.
   - Task: I needed to find out why and fix it quickly.
   - Action: I went back and found that the training data did not represent the actual variety of language used in the live documents. I collected more examples of the underrepresented categories and retrained the model.
   - Result: Accuracy went up to 79% in production within two weeks.

7. Federal compliance question
   - Situation: At MITRE, all data work had to follow strict access controls and audit trail requirements.
   - Task: I needed to make sure every step of my work was documented and traceable.
   - Action: I kept detailed logs of every data transformation, stored all code in a version control system, and made sure no raw data ever left the secure environment.
   - Result: The project passed an internal compliance audit with no findings.

8. Cross-team collaboration question
   - Situation: At the CDC, the sepsis model needed input from data engineers, clinical staff, and IT security before it could go live.
   - Task: I had to coordinate all three groups who had very different priorities.
   - Action: I set up weekly check-ins with each group separately, kept a shared document with open questions and decisions, and made sure clinical staff had final say on what the model output meant clinically.
   - Result: The model went live on schedule. All three teams said the process was smooth.

## TECHNICAL TOPICS TO PREPARE
1. ETL pipeline design using Python — the job description specifically mentions data pipelines, so be ready to explain how you build, schedule, and monitor them.
2. Machine learning model evaluation metrics — know precision, recall, F1, ROC-AUC and when to use each, because healthcare models must balance false positives and false negatives carefully.
3. SQL for large datasets — the job requires SQL, so practice writing queries with joins, window functions, and aggregations on big tables.
4. AWS services relevant to data science — SageMaker for model training and deployment, S3 for storage, Glue for ETL. The VA uses cloud infrastructure so this knowledge is directly relevant.
5. Federal data governance basics — understand what HIPAA means for data handling, what an audit trail is, and why data lineage matters in a government environment.

## BEHAVIOURAL COMPETENCIES
1. Attention to data quality
   The VA handles veteran health records where errors can affect real medical decisions. They want someone who checks their work carefully.
   Example to prepare: Talk about the automated data quality checks you built at MITRE that eliminated report errors.

2. Ability to communicate technical findings clearly
   The role requires briefing senior leadership and working with non-technical clinical staff. This is explicitly listed in the job description.
   Example to prepare: Talk about the one-page sepsis model summary you presented to CDC leadership that led to the rollout approval.

3. Collaboration across different teams
   The job involves working with clinical informatics teams, IT architects, and program officers — three very different groups.
   Example to prepare: Talk about how you coordinated the CDC sepsis model rollout across data, clinical, and IT teams at the same time.

## RED FLAGS TO ADDRESS
1. You have not worked directly at the VA before
   If asked: "You have not worked at the VA specifically — how quickly do you think you can get up to speed?"
   Answer: "I have spent my entire career supporting federal health agencies — the CDC, Booz Allen Hamilton on federal contracts, and MITRE. I am already familiar with federal compliance requirements, government data governance, and the kind of careful, documented work that agencies like the VA expect. The domain shift from CDC health data to VA veteran data is a smaller step than it might appear."

2. You may not have worked with VA-specific systems
   If asked: "Are you familiar with the VA's internal data systems like CDW or VistA?"
   Answer: "I have not worked with those systems directly, but I have worked with complex, mission-critical health data systems at the CDC. I learn new data environments quickly — in my first month at Booz Allen I had to ramp up on a client system I had never seen before and was contributing independently within three weeks."

3. Your most recent role may not be at the GS-12 seniority level
   If asked: "Can you give us examples of the kind of senior-level independent work this role requires?"
   Answer: "At the CDC I led a team of six analysts and owned the full lifecycle of the sepsis model from design to deployment. I made technical decisions independently, managed stakeholder communication, and was accountable for the final output. That is the level of ownership I am ready to bring to this role."
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
