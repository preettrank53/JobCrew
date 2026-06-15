import unittest
import os
import sys

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from graph.pipeline import compiled_graph, route_fit_score
from graph.state import FitScore

class TestGraphStructure(unittest.TestCase):
    def test_node_presence_and_count(self):
        node_keys = list(compiled_graph.nodes.keys())
        expected_nodes = [
            'input_validation', 'job_analysis', 'fit_scoring',
            'resume_generation', 'messaging', 'interview_prep',
            'skills_gap', 'company_intelligence', 'quality_evaluation',
            'output_finalization'
        ]
        
        # Verify all expected nodes are present
        for node in expected_nodes:
            self.assertIn(node, node_keys, f"Node {node} is missing from the compiled graph.")
            
        # Total nodes count check (10 user-defined nodes + __start__ + __end__ = 12 nodes)
        self.assertEqual(len(node_keys), 11, f"Expected 11 graph node definitions, got {len(node_keys)}")

    def test_entry_point(self):
        edges = [(e.source, e.target) for e in compiled_graph.get_graph().edges]
        # Verify that __start__ connects directly to input_validation
        self.assertIn(('__start__', 'input_validation'), edges, "Graph entry point must be '__start__' -> 'input_validation'.")
        
    def test_routing_edge_targets(self):
        edges = [(e.source, e.target) for e in compiled_graph.get_graph().edges]
        
        # Verify the three branches from fit_scoring are present
        self.assertIn(('fit_scoring', 'resume_generation'), edges, "Fast-track edge ('fit_scoring', 'resume_generation') missing.")
        self.assertIn(('fit_scoring', 'company_intelligence'), edges, "Standard edge ('fit_scoring', 'company_intelligence') missing.")
        self.assertIn(('fit_scoring', 'skills_gap'), edges, "Gap focus edge ('fit_scoring', 'skills_gap') missing.")

    def test_conditional_routing_function(self):
        # Test fast track (overall score >= 8.0)
        state_fast = {"candidate_profile": {}, "fit_score": FitScore(overall_score=8.5, summary="Test")}
        self.assertEqual(route_fit_score(state_fast), "fast_track")
        
        # Test standard (5.0 <= overall score < 8.0)
        state_std = {"candidate_profile": {}, "fit_score": FitScore(overall_score=7.0, summary="Test")}
        self.assertEqual(route_fit_score(state_std), "standard")
        
        # Test gap focus (overall score < 5.0)
        state_gap = {"candidate_profile": {}, "fit_score": FitScore(overall_score=4.0, summary="Test")}
        self.assertEqual(route_fit_score(state_gap), "gap_focus")

    def test_default_routing_fallback(self):
        # Test fallback when fit_score is missing
        state_none = {"candidate_profile": {}, "fit_score": None}
        self.assertEqual(route_fit_score(state_none), "standard")

if __name__ == '__main__':
    unittest.main()
