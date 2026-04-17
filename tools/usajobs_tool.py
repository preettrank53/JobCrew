import requests
import json
import os
import sys

# Add the parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import USAJOBS_API_KEY, USAJOBS_USER_AGENT

def fetch_jobs(keyword: str, location: str = "", results_per_page: int = 10) -> list[dict]:
    """
    Fetches job listings from the USAJobs API.
    """
    url = "https://data.usajobs.gov/api/search"
    
    headers = {
        "Authorization-Key": USAJOBS_API_KEY or "",
        "User-Agent": USAJOBS_USER_AGENT or ""
    }
    
    params = {
        "Keyword": keyword,
        "ResultsPerPage": results_per_page
    }
    
    if location:
        params["LocationName"] = location
        
    try:
        response = requests.get(url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"HTTP request to USAJobs API failed: {str(e)}")
        
    if response.status_code != 200:
        raise RuntimeError(f"USAJobs API returned non-200 status code: {response.status_code}. Response: {response.text}")
        
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("USAJobs API response is not valid JSON.")
        
    if "SearchResult" not in data or "SearchResultItems" not in data["SearchResult"]:
        raise ValueError("Malformed USAJobs API response: missing expected 'SearchResult' or 'SearchResultItems' keys.")
        
    items = data["SearchResult"]["SearchResultItems"]
    
    if not items:
        return []
        
    parsed_jobs = []
    for item in items:
        desc = item.get("MatchedObjectDescriptor", {})
        
        # Safely extract location
        locations = desc.get("PositionLocation", [])
        loc_str = locations[0].get("LocationName", "Unknown") if locations else "Unknown"
        
        # Safely extract remuneration
        remunerations = desc.get("PositionRemuneration", [])
        salary_min = remunerations[0].get("MinimumRange", "N/A") if remunerations else "N/A"
        salary_max = remunerations[0].get("MaximumRange", "N/A") if remunerations else "N/A"
        
        # Safely extract description
        user_area = desc.get("UserArea", {}).get("Details", {})
        description = user_area.get("JobSummary", "No description provided.")
        
        job_data = {
            "title": desc.get("PositionTitle", "Unknown Title"),
            "department": desc.get("DepartmentName", "Unknown Department"),
            "location": loc_str,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "close_date": desc.get("ApplicationCloseDate", "Unknown"),
            "job_id": desc.get("PositionID", item.get("MatchedObjectId", "Unknown ID")),
            "apply_url": desc.get("PositionURI", "Unknown URL"),
            "description": description
        }
        parsed_jobs.append(job_data)
        
    return parsed_jobs

if __name__ == "__main__":
    # Test block
    print("Testing fetch_jobs with keyword 'software engineer'...")
    try:
        jobs = fetch_jobs("software engineer")
        print(f"Results found: {len(jobs)}")
        if jobs:
            print(f"Title of first result: {jobs[0]['title']}")
    except Exception as e:
        print(f"Error testing fetch_jobs: {e}")
