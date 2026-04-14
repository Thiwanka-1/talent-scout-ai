import unittest
import json
from student3_interviewer.s3_tool import format_interview_topics

class TestInterviewerTool(unittest.TestCase):
    
    def setUp(self):
        """Define standard test parameters."""
        self.role = "Senior Cloud Engineer"

    def test_standard_missing_skills(self):
        """Test case 1: Tool correctly formats standard missing skills."""
        missing = "Kubernetes, Terraform"
        result = format_interview_topics.run(missing_skills=missing, role_title=self.role)
        
        self.assertIn("DIRECTIVE GENERATED", result)
        self.assertIn("SKILL GAP DETECTED", result)
        self.assertIn("Kubernetes", result)
        self.assertIn("Terraform", result)

    def test_messy_list_input(self):
        """Test case 2: Tool correctly handles stringified arrays (common LLM artifact)."""
        missing = "['AWS', 'Docker']"
        result = format_interview_topics.run(missing_skills=missing, role_title=self.role)
        
        self.assertIn("DIRECTIVE GENERATED", result)
        # We verify the clean words made it into the final JSON output
        self.assertIn('"AWS"', result)
        self.assertIn('"Docker"', result)
        # Verify the messy single quotes from the input were removed
        self.assertNotIn("'AWS'", result)

    def test_perfect_candidate_handling(self):
        """Test case 3: Tool correctly pivots strategy when no skills are missing."""
        result_empty = format_interview_topics.run(missing_skills="", role_title=self.role)
        result_none = format_interview_topics.run(missing_skills="None", role_title=self.role)
        
        # Both should trigger the PERFECT MATCH scenario
        self.assertIn("PERFECT MATCH DETECTED", result_empty)
        self.assertIn("PERFECT MATCH DETECTED", result_none)
        self.assertIn("advanced architectural", result_none)

if __name__ == '__main__':
    print("Executing Comprehensive Test Suite for Module 3 (Interviewer)...")
    unittest.main()