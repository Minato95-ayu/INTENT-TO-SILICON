import sys
import os
import pytest
from unittest.mock import patch
from tools.cli import main

def test_cli_build(tmp_path):
    with patch('sys.argv', ['aayu', 'build', 'examples/crm.aayu']):
        try:
            main()
        except SystemExit:
            pass

def test_cli_help():
    with patch('sys.argv', ['aayu', '--help']):
        try:
            main()
        except SystemExit:
            pass
