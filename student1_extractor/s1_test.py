import unittest
import os
from student1_extractor.s1_tool import read_local_document

class TestResumeParserTool(unittest.TestCase):
    
    def setUp(self):
        """Pre-test environment configuration."""
        self.valid_file = 'mock_valid_resume.txt'
        self.empty_file = 'mock_empty_resume.txt'
        self.invalid_ext_file = 'mock_resume.pdf'
        
        # Seed mock files
        with open(self.valid_file, 'w', encoding='utf-8') as f:
            f.write("Candidate: Alice\nExperience: 5 years\nSkills: Python, Node.js, Docker, React")
            
        with open(self.empty_file, 'w', encoding='utf-8') as f:
            f.write("")
            
        with open(self.invalid_ext_file, 'w', encoding='utf-8') as f:
            f.write("Fake PDF data")

    def test_successful_read(self):
        """Test case 1: Validate standard successful extraction."""
        result = read_local_document.run(file_path=self.valid_file)
        self.assertIn("SUCCESSFUL EXTRACTION", result)
        self.assertIn("Node.js", result)

    def test_file_not_found(self):
        """Test case 2: Validate error handling for missing files."""
        result = read_local_document.run(file_path="non_existent_file_path.txt")
        self.assertIn("CRITICAL ERROR: File not found", result)

    def test_unsupported_extension(self):
        """Test case 3: Validate security check against unauthorized file types."""
        result = read_local_document.run(file_path=self.invalid_ext_file)
        self.assertIn("ERROR: Unsupported file format", result)
        
    def test_empty_file_handling(self):
        """Test case 4: Validate handling of blank documents."""
        result = read_local_document.run(file_path=self.empty_file)
        self.assertIn("WARNING", result)
        self.assertIn("completely empty", result)

    def tearDown(self):
        """Post-test cleanup of mock artifacts."""
        for file in [self.valid_file, self.empty_file, self.invalid_ext_file]:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    print("Executing Comprehensive Test Suite for Module 1 (Extractor)...")
    unittest.main()