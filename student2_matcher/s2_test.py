import unittest
import json
from student2_matcher.s2_tool import calculate_skill_match

class TestMatcherTool(unittest.TestCase):
    
    def setUp(self):
        """Define the static job requirements for testing."""
        self.job_reqs = "Python, React, MongoDB, Docker, AWS"

    def test_perfect_match(self):
        """Test case 1: Candidate has all required skills."""
        resume = "Python, AWS, Docker, MongoDB, React, ExtraSkill"
        result = calculate_skill_match.run(resume_skills=resume, job_skills=self.job_reqs)
        
        self.assertIn("ANALYSIS COMPLETE", result)
        self.assertIn('"match_percentage": 100.0', result)
        self.assertIn('"missing_skills": []', result)

    def test_partial_match_with_capitalization(self):
        """Test case 2: Candidate has partial skills with messy capitalization."""
        resume = " pYthOn , rEaCt, HTML, CSS"
        result = calculate_skill_match.run(resume_skills=resume, job_skills=self.job_reqs)
        
        self.assertIn('"match_percentage": 40.0', result)
        self.assertIn("mongodb", result.lower()) # Should flag missing skills
        self.assertIn("docker", result.lower())

    def test_zero_match_empty_resume(self):
        """Test case 3: Candidate resume failed to parse or is completely empty."""
        resume = "   "
        result = calculate_skill_match.run(resume_skills=resume, job_skills=self.job_reqs)
        
        self.assertIn('"match_percentage": 0.0', result)
        self.assertTrue("python" in result.lower() and "aws" in result.lower())

    def test_empty_job_requirements(self):
        """Test case 4: System error where job requirements are missing (Division by Zero check)."""
        resume = "Python, React"
        result = calculate_skill_match.run(resume_skills=resume, job_skills="")
        self.assertIn("CRITICAL ERROR", result)

if __name__ == '__main__':
    print("Executing Comprehensive Test Suite for Module 2 (Matcher)...")
    unittest.main()