import unittest
from unittest.mock import patch, MagicMock
import requests
from tools.usajobs_tool import fetch_jobs

class TestFetchJobs(unittest.TestCase):
    @patch('requests.get')
    def test_successful_fetch_returns_list(self, mock_get):
        # Mock successful response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "SearchResult": {
                "SearchResultItems": [
                    {
                        "MatchedObjectDescriptor": {
                            "PositionTitle": "Data Analyst",
                            "DepartmentName": "Department of Labor",
                            "PositionLocation": [{"LocationName": "Washington, DC"}],
                            "PositionRemuneration": [{"MinimumRange": "80000", "MaximumRange": "120000"}],
                            "ApplicationCloseDate": "2026-12-31",
                            "PositionID": "DOL-1",
                            "PositionURI": "https://usajobs.gov/job/1",
                            "UserArea": {"Details": {"JobSummary": "Analyze labor data."}}
                        }
                    },
                    {
                        "MatchedObjectDescriptor": {
                            "PositionTitle": "Senior Analyst",
                            "DepartmentName": "Department of Labor",
                            "PositionLocation": [{"LocationName": "Remote"}],
                            "PositionRemuneration": [{"MinimumRange": "100000", "MaximumRange": "150000"}],
                            "ApplicationCloseDate": "2026-11-30",
                            "PositionID": "DOL-2",
                            "PositionURI": "https://usajobs.gov/job/2",
                            "UserArea": {"Details": {"JobSummary": "Lead data analysis."}}
                        }
                    }
                ]
            }
        }
        mock_get.return_value = mock_response

        results = fetch_jobs(keyword="analyst", results_per_page=2)
        
        self.assertIsInstance(results, list)
        self.assertEqual(len(results), 2)
        
        required_keys = ['title', 'department', 'location', 'salary_min', 'salary_max', 'close_date', 'job_id', 'apply_url', 'description']
        for job in results:
            for key in required_keys:
                self.assertIn(key, job)

    @patch('requests.get')
    def test_http_error_raises_exception(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            fetch_jobs(keyword="test")

    @patch('requests.get')
    def test_empty_results_returns_empty_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "SearchResult": {
                "SearchResultItems": []
            }
        }
        mock_get.return_value = mock_response
        
        results = fetch_jobs(keyword="nonexistent")
        self.assertEqual(results, [])

    @patch('requests.get')
    def test_malformed_response_raises_exception(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"Something": "Else"}
        mock_get.return_value = mock_response
        
        with self.assertRaises(Exception):
            fetch_jobs(keyword="test")

    @patch('requests.get')
    def test_keyword_is_passed_as_query_param(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"SearchResult": {"SearchResultItems": []}}
        mock_get.return_value = mock_response
        
        fetch_jobs(keyword="software engineer", location="Washington DC")
        
        # Check call arguments
        args, kwargs = mock_get.call_args
        params = kwargs.get('params', {})
        self.assertEqual(params.get('Keyword'), "software engineer")
        self.assertEqual(params.get('LocationName'), "Washington DC")

if __name__ == '__main__':
    unittest.main()
