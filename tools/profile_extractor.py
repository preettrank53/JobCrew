import json
import hashlib
from config.llm import llm
from tools.resume_parser import parse_resume_file

_profile_cache = {}

def get_cached_profile_extraction(resume_text):
    text_hash = hashlib.md5(resume_text.encode()).hexdigest()
    if text_hash in _profile_cache:
        return _profile_cache[text_hash]
    
    result = extract_profile_from_resume(resume_text)
    _profile_cache[text_hash] = result
    return result

def extract_profile_from_resume(resume_text):
    prompt = f"""You are an expert resume parser. Your task is to extract four specific fields from the resume provided below.
You MUST respond with a valid JSON object. Do NOT include any additional text, preamble, or markdown formatting outside of the JSON block.

Extract the following four keys exactly as named:
- "name": The full name of the candidate as a single string.
- "experience": All work experience entries formatted as a structured bullet list, each entry containing job title, company, duration, and two to three key responsibilities.
- "skills": A comma separated list of all technical skills, tools, programming languages, frameworks, and soft skills found in the resume.
- "education": All education entries formatted as degree name, institution, and graduation year.

---RESUME START---
{resume_text}
---RESUME END---
"""
    try:
        response = llm.call(messages=[{"role": "user", "content": prompt}])
        raw_text = str(response).strip()
        
        # Clean markdown code fences if present
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        
        try:
            parsed_data = json.loads(raw_text)
        except json.JSONDecodeError:
            raise ValueError(f"LLM returned malformed JSON — profile extraction failed.\nRaw Response: {raw_text}")
            
        required_keys = ['name', 'experience', 'skills', 'education']
        missing_keys = [k for k in required_keys if k not in parsed_data or not parsed_data[k]]
        
        if missing_keys:
            raise ValueError(f"Incomplete profile extracted — missing fields: {', '.join(missing_keys)}")
            
        return parsed_data
        
    except ValueError as ve:
        raise ve
    except Exception as e:
        raise ValueError(f"LLM Profile Extraction failed: {str(e)}")

def build_profile_from_upload(uploaded_file):
    resume_text = parse_resume_file(uploaded_file)
    profile = extract_profile_from_resume(resume_text)
    return profile

if __name__ == "__main__":
    sample_resume = """
    John Doe
    San Francisco, CA | johndoe@email.com | 555-0102
    
    EXPERIENCE
    Data Scientist - Tech Innovators Inc.
    Jan 2020 - Present
    - Developed machine learning models to predict customer churn with 85% accuracy.
    - Optimized SQL queries resulting in a 20% reduction in database load times.
    - Collaborated with cross-functional teams to deploy real-time analytics dashboards.
    
    SKILLS
    Python, SQL, Machine Learning, TensorFlow, Pandas, Tableau, Communication
    
    EDUCATION
    Master of Science in Computer Science
    University of California, Berkeley
    Graduated: 2019
    """
    
    print("Testing Profile Extractor...\n")
    try:
        profile = extract_profile_from_resume(sample_resume)
        print("Success! Extracted Profile:\n")
        print(json.dumps(profile, indent=2))
    except Exception as e:
        print(f"Error: {e}")
