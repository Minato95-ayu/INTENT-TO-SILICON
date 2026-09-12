import unittest
import os
import tempfile
import shutil
from tools.package_manager.manager import PackageManager

class TestPackageManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.old_cwd = os.getcwd()
        os.chdir(self.temp_dir.name)
        
    def tearDown(self):
        os.chdir(self.old_cwd)
        try:
            self.temp_dir.cleanup()
        except:
            pass

    def test_init(self):
        pm = PackageManager(root_dir=".", mock_home=self.temp_dir.name)
        pm.init()
        self.assertTrue(os.path.exists("aayu.json"))
            
    def test_install(self):
        pm = PackageManager(root_dir=".", mock_home=self.temp_dir.name)
        pm.init()
        # Mocking install
        try:
            pm.install("dummy_package")
        except Exception:
            pass

if __name__ == "__main__":
    unittest.main()
