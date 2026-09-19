# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

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
