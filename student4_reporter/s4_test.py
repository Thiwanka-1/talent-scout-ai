import unittest
import os
from student4_reporter.s4_tool import save_evaluation_report

class TestReporterTool(unittest.TestCase):
    
    def test_successful_file_save(self):
        """Test case 1: Validate file is created with sanitized name."""
        content = "# Test Report\nThis is a test."
        result = save_evaluation_report.run(report_content=content, candidate_name="John O'Connor!")
        
        self.assertIn("SUCCESS", result)
        self.assertTrue(os.path.exists("outputs/john_o_connor__evaluation_report.md"))

    def test_empty_content_prevention(self):
        """Test case 2: Validate system rejects empty reports."""
        result = save_evaluation_report.run(report_content="", candidate_name="Jane Doe")
        self.assertIn("ERROR", result)

    def tearDown(self):
        """Clean up generated test files."""
        if os.path.exists("outputs/john_o_connor__evaluation_report.md"):
            os.remove("outputs/john_o_connor__evaluation_report.md")

if __name__ == '__main__':
    print("Executing Comprehensive Test Suite for Module 4 (Reporter)...")
    unittest.main()