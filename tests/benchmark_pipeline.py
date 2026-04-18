import sys
import os
import time
import datetime

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew import run_jobcrew_pipeline
from tests.prompt_quality_test import (
    TEST_JOB_SAMPLES,
    TEST_CANDIDATE_PROFILE,
    score_job_analysis_output,
    score_resume_output,
    score_messaging_output
)

SAMPLE_JOB = TEST_JOB_SAMPLES[0]
SAMPLE_CANDIDATE = TEST_CANDIDATE_PROFILE

def run_benchmark():
    print("=" * 60)
    print("JOBCREW PIPELINE BENCHMARK")
    print("=" * 60)
    
    # --- Standard Mode ---
    print("\n[1/2] Running STANDARD mode...")
    standard_start = time.time()
    try:
        standard_result = run_jobcrew_pipeline(SAMPLE_JOB, SAMPLE_CANDIDATE, fast_mode=False)
    except Exception as e:
        print(f"Standard mode failed: {e}")
        return
    standard_end = time.time()
    standard_time = round(standard_end - standard_start, 2)
    print(f"Standard mode completed in {standard_time}s")
    
    # --- Fast Mode ---
    print("\n[2/2] Running FAST mode...")
    fast_start = time.time()
    try:
        fast_result = run_jobcrew_pipeline(SAMPLE_JOB, SAMPLE_CANDIDATE, fast_mode=True)
    except Exception as e:
        print(f"Fast mode failed: {e}")
        return
    fast_end = time.time()
    fast_time = round(fast_end - fast_start, 2)
    print(f"Fast mode completed in {fast_time}s")
    
    # --- Quality Scores ---
    std_ja = score_job_analysis_output(standard_result.get("job_analysis", ""))
    std_res = score_resume_output(standard_result.get("resume_and_cover_letter", ""))
    std_msg = score_messaging_output(standard_result.get("linkedin_message", ""))
    
    fast_ja = score_job_analysis_output(fast_result.get("job_analysis", ""))
    fast_res = score_resume_output(fast_result.get("resume_and_cover_letter", ""))
    fast_msg = score_messaging_output(fast_result.get("linkedin_message", ""))
    
    # --- Speed improvement ---
    if standard_time > 0:
        speed_improvement = round(((standard_time - fast_time) / standard_time) * 100, 1)
    else:
        speed_improvement = 0.0
    
    # --- Build Report ---
    report_lines = [
        "=" * 60,
        "JOBCREW PIPELINE BENCHMARK REPORT",
        f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Job: {SAMPLE_JOB['title']} at {SAMPLE_JOB['department']}",
        "=" * 60,
        "",
        "EXECUTION TIME",
        f"  Standard Mode: {standard_time}s",
        f"  Fast Mode:     {fast_time}s",
        f"  Speed Improvement: {speed_improvement}%",
        "",
        "QUALITY SCORES - STANDARD MODE",
        f"  Job Analysis:    {std_ja['score']}/{std_ja['max_score']} [{'PASS' if std_ja['passed'] else 'FAIL'}]",
        f"  Resume:          {std_res['score']}/{std_res['max_score']} [{'PASS' if std_res['passed'] else 'FAIL'}]",
        f"  Messaging:       {std_msg['score']}/{std_msg['max_score']} [{'PASS' if std_msg['passed'] else 'FAIL'}]",
        "",
        "QUALITY SCORES - FAST MODE",
        f"  Job Analysis:    {fast_ja['score']}/{fast_ja['max_score']} [{'PASS' if fast_ja['passed'] else 'FAIL'}]",
        f"  Resume:          {fast_res['score']}/{fast_res['max_score']} [{'PASS' if fast_res['passed'] else 'FAIL'}]",
        f"  Messaging:       {fast_msg['score']}/{fast_msg['max_score']} [{'PASS' if fast_msg['passed'] else 'FAIL'}]",
        "",
        "=" * 60,
    ]
    
    report = "\n".join(report_lines)
    print("\n" + report)
    
    # --- Save report ---
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_path = os.path.join('logs', f"benchmark_{timestamp}.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    run_benchmark()
