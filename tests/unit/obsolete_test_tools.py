import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../tools')))

from tools.cli_formatter import AAYUFormatter
from tools.cli_linter import AAYULinter

class TestDeveloperTools(unittest.TestCase):
    
    def test_formatter(self):
        """
        Tests if the AAYU Formatter correctly indents blocks and handles whitespace.
        """
        raw_code = "entity User\\n  has\\nid: Number\\n    name: Text\\nend."
        
        expected = "entity User\\nhas\\n    id: Number\\n    name: Text\\nend."
        
        formatter = AAYUFormatter()
        result = formatter.format(raw_code.replace("\\n", "\n"))
        self.assertEqual(result, expected.replace("\\n", "\n"))

    def test_linter_missing_period(self):
        """
        Tests if the AAYULinter catches missing periods (.) at the end of statements.
        """
        raw_code = "let x: Number = 5\nprint(x)" # Missing periods
        linter = AAYULinter()
        diagnostics = linter.lint(raw_code)
        
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue("Missing terminating period" in diagnostics[0])
        
    def test_linter_missing_types(self):
        """
        Tests if the AAYULinter enforces strict typing on variable declarations.
        """
        raw_code = "let x = 5.\nmut y = 10." # Missing types
        linter = AAYULinter()
        diagnostics = linter.lint(raw_code)
        
        self.assertEqual(len(diagnostics), 2)
        self.assertTrue("Missing type annotation" in diagnostics[0])
        
    def test_linter_clean_code(self):
        """
        Tests that clean code produces zero diagnostics.
        """
        raw_code = "let x: Number = 5.\nprint(x)."
        linter = AAYULinter()
        diagnostics = linter.lint(raw_code)
        
        self.assertEqual(len(diagnostics), 0)

if __name__ == '__main__':
    unittest.main()
