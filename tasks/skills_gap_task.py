from crewai import Task

def create_skills_gap_task(agent, job_analysis_output, candidate_profile, job_data):
    return Task(
        description=f"""
Carefully read the job analysis output, the candidate's complete profile, and the original job details.

Job Title: {job_data.get('title')}
Department: {job_data.get('department')}

Job Analysis Output:
{job_analysis_output}

Candidate Profile:
Name: {candidate_profile.get('name')}
Experience: {candidate_profile.get('experience')}
Skills: {candidate_profile.get('skills')}
Education: {candidate_profile.get('education')}

Your task is to perform a three-level skill comparison:
1. Level 1 - Hard Skills: technical tools, programming languages, software, platforms mentioned in mandatory requirements versus what the candidate explicitly lists in their skills field.
2. Level 2 - Soft Skills: leadership, communication, collaboration, and management competencies mentioned in the job versus what is evident in the candidate's experience descriptions.
3. Level 3 - Domain Knowledge: subject matter expertise, industry knowledge, and specialized experience required by the role versus what the candidate's background demonstrates.

For each identified gap classify it by severity:
- Critical - mandatory requirement the candidate clearly lacks, will likely disqualify application.
- Important - preferred qualification the candidate lacks, weakens the application.
- Minor - nice-to-have that would strengthen but not having it is acceptable.

For each gap regardless of severity provide:
- A specific free or low-cost course or certification to close it — name the exact course, platform, and estimated completion time.
- A realistic timeline to close the gap — be honest, do not say "2 weeks" for something that takes 6 months.
- A quick win tip — one thing the candidate can do immediately (this week) to partially address the gap.

Also identify the candidate's existing strengths that directly match requirements — frame these as competitive advantages to emphasize in the application.

CRITICAL INSTRUCTION: Be completely honest about gaps even if it means telling the candidate they are not well qualified — do not sugarcoat critical gaps.
""",
        expected_output="""\
## SKILLS GAP ANALYSIS REPORT
## QUICK MATCH SUMMARY
Overall Fit Score: [X/10]
Strong Match: [count] requirements
Partial Match: [count] requirements  
Missing: [count] requirements

## YOUR COMPETITIVE ADVANTAGES
[Bullet list of 4-6 skills/experiences the candidate has that directly match requirements — frame each as a talking point]

## CRITICAL GAPS 
[Only include if any critical gaps exist — skip section if none]
### Gap 1: [Skill/Knowledge Name]
- **What they want:** [exact requirement from job]
- **What you have:** [honest assessment of candidate's current level]
- **Recommended Resource:** [specific course/cert name, platform, cost, duration]
- **Realistic Timeline:** [honest timeframe]
- **Quick Win This Week:** [one immediate action]

## IMPORTANT GAPS 
### Gap [n]: [Skill/Knowledge Name]
[same structure as critical gaps]

## MINOR GAPS 
### Gap [n]: [Skill/Knowledge Name]
[same structure]

## LEARNING ROADMAP
### Phase 1 — Immediate (This Week)
[2-3 specific actions the candidate can take right now]
### Phase 2 — Short Term (1-3 Months)
[3-4 specific courses or projects to complete]
### Phase 3 — Long Term (3-12 Months)
[2-3 certifications or deeper learning paths]

## HONEST ASSESSMENT
[3-4 sentences of direct, honest advice about this candidate's realistic chances for this specific role, what their biggest strengths are, what their most important gap is, and whether they should apply now or build skills first]
""",
        agent=agent
    )
