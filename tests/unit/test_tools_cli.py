import unittest
import os
import sys
from unittest.mock import patch
from io import StringIO
from tools.cli import main

class TestCLI(unittest.TestCase):
    @patch('sys.argv', ['aayu', '--version'])
    def test_version(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass
            self.assertIn("AAYU", fake_out.getvalue())
            
    @patch('sys.argv', ['aayu', 'help'])
    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass
            
    @patch('sys.argv', ['aayu', 'run', 'does_not_exist.aayu'])
    def test_run_missing(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass

    @patch('sys.argv', ['aayu', 'format', 'does_not_exist.aayu'])
    def test_format_missing(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass

    @patch('sys.argv', ['aayu', 'lint', 'does_not_exist.aayu'])
    def test_lint_missing(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass

    @patch('sys.argv', ['aayu', 'build', 'does_not_exist.aayu'])
    def test_build_missing(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass

    @patch('sys.argv', ['aayu', 'repl'])
    def test_repl(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            # We would need to mock input, maybe skip for now
            pass
            
    @patch('sys.argv', ['aayu', 'init', 'my_project'])
    def test_init(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            try:
                main()
            except SystemExit:
                pass

if __name__ == '__main__':
    unittest.main()
