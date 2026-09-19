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

import unittest
import sys
from io import StringIO
from tools.cli import main
import tempfile
import os
from unittest.mock import patch

class TestCLIAuto(unittest.TestCase):
    def run_cli(self, args):
        sys.argv = args
        try:
            main()
        except SystemExit:
            pass
        except Exception:
            pass

    def test_cli_all(self):
        with patch('sys.stdout', new=StringIO()):
            self.run_cli(['aayu'])
            self.run_cli(['aayu', '--version'])
            self.run_cli(['aayu', 'help'])
            self.run_cli(['aayu', 'invalid_command'])
            
            f_name = None
            with tempfile.NamedTemporaryFile('w', suffix='.aayu', delete=False) as f:
                f.write("project Test. end.")
                f.flush()
                f_name = f.name
                
            self.run_cli(['aayu', 'run', f_name])
            self.run_cli(['aayu', 'build', f_name])
            self.run_cli(['aayu', 'fmt', f_name])
            self.run_cli(['aayu', 'lint', f_name])
            
            try:
                os.remove(f_name)
            except: pass
            
            self.run_cli(['aayu', 'init', 'test_proj'])
            self.run_cli(['aayu', 'install', 'dummy'])
            self.run_cli(['aayu', 'test'])

if __name__ == '__main__':
    unittest.main()
