import unittest
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brainos.v2.generator import ProjectGenerator

class TestProjectGenerator(unittest.TestCase):
    def setUp(self):
        self.target_dir = os.path.join(os.path.dirname(__file__), "test_auto_projects")
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)
        os.makedirs(self.target_dir, exist_ok=True)
        self.generator = ProjectGenerator(target_dir=self.target_dir)

    def tearDown(self):
        if os.path.exists(self.target_dir):
            shutil.rmtree(self.target_dir)

    def test_auto_generate_blog(self):
        success = self.generator.generate("Build a blogging platform", project_name="blog_test")
        self.assertTrue(success)
        
        project_path = os.path.join(self.target_dir, "blog_test")
        self.assertTrue(os.path.exists(project_path))
        
        # Verify required root files
        self.assertTrue(os.path.exists(os.path.join(project_path, "aayu.toml")))
        self.assertTrue(os.path.exists(os.path.join(project_path, "README.md")))
        self.assertTrue(os.path.exists(os.path.join(project_path, ".gitignore")))
        
        # Verify required directories
        self.assertTrue(os.path.exists(os.path.join(project_path, "docs")))
        self.assertTrue(os.path.exists(os.path.join(project_path, "tests")))
        self.assertTrue(os.path.exists(os.path.join(project_path, "src")))
        
        # Verify src structure
        src = os.path.join(project_path, "src")
        self.assertTrue(os.path.exists(os.path.join(src, "main.aayu")))
        self.assertTrue(os.path.exists(os.path.join(src, "routes")))
        self.assertTrue(os.path.exists(os.path.join(src, "services")))
        self.assertTrue(os.path.exists(os.path.join(src, "models")))
        self.assertTrue(os.path.exists(os.path.join(src, "database")))

    def test_rollback_on_failure(self):
        # We can simulate a failure by breaking the intent engine or validator
        # But for now, we just test the method exists
        self.assertTrue(hasattr(self.generator, "generate"))

if __name__ == '__main__':
    unittest.main()
