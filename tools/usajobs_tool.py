import requests
import json
import os
import sys
import time

# Add the parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import USAJOBS_API_KEY, USAJOBS_USER_AGENT

_jobs_cache = {}

def _build_cache_key(keyword: str, location: str, results_per_page: int) -> str:
    return f"{keyword}|{location}|{results_per_page}".lower().strip()

def _is_cache_valid(cache_key: str, max_age_seconds: int = 300) -> bool:
    if cache_key not in _jobs_cache:
        return False
    age = time.time() - _jobs_cache[cache_key]['timestamp']
    return age < max_age_seconds

def clear_jobs_cache():
    global _jobs_cache
    _jobs_cache.clear()
    print("[Cache] All cached job results cleared")

def get_cache_stats() -> dict:
    current_time = time.time()
    total_entries = len(_jobs_cache)
    valid_entries = sum(1 for entry in _jobs_cache.values() if (current_time - entry['timestamp']) < 300)
    expired_entries = total_entries - valid_entries
    keywords_cached = [entry['keyword'] for entry in _jobs_cache.values()]
    
    return {
        "total_entries": total_entries,
        "valid_entries": valid_entries,
        "expired_entries": expired_entries,
        "keywords_cached": keywords_cached
    }

def fetch_jobs(keyword: str, location: str = "", results_per_page: int = 10) -> list[dict]:
    """
    Fetches job listings from the USAJobs API.
    """
    cache_key = _build_cache_key(keyword, location, results_per_page)
    
    if _is_cache_valid(cache_key):
        print(f"[Cache HIT] Returning cached results for: {keyword}")
        return _jobs_cache[cache_key]['data']
        
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
        
    max_attempts = 3
    response = None
    last_error = None
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                last_error = f"Rate limited (HTTP 429)"
                if attempt < max_attempts - 1:
                    time.sleep(5)
                continue
            else:
                raise RuntimeError(f"USAJobs API returned non-200 status code: {response.status_code}. Response: {response.text}")
                
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            last_error = str(e)
            if attempt < max_attempts - 1:
                time.sleep(2)
            continue
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"HTTP request to USAJobs API failed: {str(e)}")
            
    if response is None or response.status_code != 200:
        raise RuntimeError(f"Failed to fetch jobs after {max_attempts} attempts. Last error: {last_error}")
        
    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("USAJobs API response is not valid JSON.")
        
    if "SearchResult" not in data or "SearchResultItems" not in data["SearchResult"]:
        raise ValueError("Malformed USAJobs API response: missing expected 'SearchResult' or 'SearchResultItems' keys.")
        
    items = data["SearchResult"]["SearchResultItems"]
    
    parsed_jobs = []
    if items:
        for item in items:
            desc = item.get("MatchedObjectDescriptor", {})
            
            locations = desc.get("PositionLocation", [])
            loc_str = locations[0].get("LocationName", "Unknown") if locations else "Unknown"
            
            remunerations = desc.get("PositionRemuneration", [])
            salary_min = remunerations[0].get("MinimumRange", "N/A") if remunerations else "N/A"
            salary_max = remunerations[0].get("MaximumRange", "N/A") if remunerations else "N/A"
            
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
            
    _jobs_cache[cache_key] = {
        'data': parsed_jobs,
        'timestamp': time.time(),
        'keyword': keyword,
        'location': location
    }
    
    print(f"[Cache MISS] Fetched {len(parsed_jobs)} jobs from USAJobs API for: {keyword}")
    
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
