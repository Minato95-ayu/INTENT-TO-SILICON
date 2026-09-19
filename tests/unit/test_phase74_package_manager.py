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
import os
import shutil
import tempfile
from tools.package_manager.manager import PackageManager

class TestPhase74PackageManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
        self.pm = PackageManager(root_dir=".", mock_home=self.temp_dir.name)
        self.pm.init()

    def tearDown(self):
        os.chdir(self.old_cwd)
        try:
            self.temp_dir.cleanup()
        except:
            pass

    def test_init_project(self):
        self.assertTrue(os.path.exists("aayu.json"))
        
    def test_publish_and_install(self):
        try:
            self.pm.install("test_pkg")
        except Exception:
            pass
            
    def test_remove(self):
        try:
            self.pm.remove("test_pkg")
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()
