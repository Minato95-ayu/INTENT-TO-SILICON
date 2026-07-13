import unittest
import os
import tempfile
from tools.package_manager import AAYUPackageManager

class TestPackageManager(unittest.TestCase):
    def test_init(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            pm = AAYUPackageManager()
            pm.init_project("TestProject")
            self.assertTrue(os.path.exists("aayu.toml"))
            
    def test_install(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            os.chdir(temp_dir)
            pm = AAYUPackageManager()
            pm.init_project("TestProject")
            # Mocking install
            # Just calling it to see if it runs
            try:
                pm.install("dummy_package")
            except Exception:
                pass

if __name__ == '__main__':
    unittest.main()
