"""
=============================================================================
FILE: test_phase74_package_manager.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import unittest
import os
import sys
import shutil
import json
import tempfile
from unittest.mock import patch

# Add prototype to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import tools.package_manager as package_manager
from tools.package_manager import AAYUPackageManager

def mock_get_global_aayu_dir():
    path = os.path.join(os.getcwd(), '.aayu_global')
    os.makedirs(os.path.join(path, "registry", "index"), exist_ok=True)
    os.makedirs(os.path.join(path, "cache"), exist_ok=True)
    return path

def mock_get_local_project_dir():
    path = os.getcwd()
    os.makedirs(os.path.join(path, ".aayu", "packages"), exist_ok=True)
    return path

class TestPhase74PackageManager(unittest.TestCase):
    def setUp(self):
        # Setup a temporary environment
        self.temp_dir = tempfile.mkdtemp()
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        self.patcher1 = patch('tools.package_manager.get_global_aayu_dir', side_effect=mock_get_global_aayu_dir)
        self.patcher2 = patch('tools.package_manager.get_local_project_dir', side_effect=mock_get_local_project_dir)
        self.patcher1.start()
        self.patcher2.start()
        
        self.pm = AAYUPackageManager()
        self.pm.init_project('test_project')

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()
        os.chdir(self.old_cwd)
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

    def test_init_project(self):
        self.assertTrue(os.path.exists('aayu.toml'))
        data = self.pm._read_toml('aayu.toml')
        self.assertEqual(data['name'], 'test_project')

    def test_publish_and_install(self):
        # 1. Create a dummy package to publish
        os.makedirs('dummy_pkg')
        with open('dummy_pkg/aayu.toml', 'w') as f:
            f.write('''name = "dummy_pkg"\nversion = "1.0.0"\n''')
        with open('dummy_pkg/main.aayu', 'w') as f:
            f.write('''print("hello dummy").\n''')
            
        old_local = self.pm.local_dir
        self.pm.local_dir = os.path.join(self.temp_dir, 'dummy_pkg')
        self.pm.aayu_toml_path = os.path.join(self.pm.local_dir, 'aayu.toml')
        self.pm.publish()
        
        # Restore local project
        self.pm.local_dir = old_local
        self.pm.aayu_toml_path = os.path.join(self.pm.local_dir, 'aayu.toml')
        
        # Check registry was updated
        idx = self.pm._get_registry_index('dummy_pkg')
        self.assertIsNotNone(idx)
        self.assertIn('1.0.0', idx['versions'])
        
        # 2. Install the package
        self.pm.install('dummy_pkg', '1.0.0')
        
        # Check aayu.toml updated
        data = self.pm._read_toml('aayu.toml')
        self.assertIn('dummy_pkg', data['dependencies'])
        
        # Check lockfile generated
        lock = self.pm._read_toml('aayu.lock')
        self.assertIn('dummy_pkg', lock['packages'])
        
        # Check package extracted
        self.assertTrue(os.path.exists('.aayu/packages/dummy_pkg/main.aayu'))

    def test_remove(self):
        # Manually add to aayu.toml
        data = self.pm._read_toml('aayu.toml')
        data['dependencies'] = {'dummy_pkg': '1.0.0'}
        self.pm._write_toml('aayu.toml', data)
        os.makedirs('.aayu/packages/dummy_pkg')
        
        self.pm.remove('dummy_pkg')
        
        # Check removed
        data = self.pm._read_toml('aayu.toml')
        self.assertNotIn('dummy_pkg', data['dependencies'])
        self.assertFalse(os.path.exists('.aayu/packages/dummy_pkg'))

if __name__ == '__main__':
    unittest.main()
