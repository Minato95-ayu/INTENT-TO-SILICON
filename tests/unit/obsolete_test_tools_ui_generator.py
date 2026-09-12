import unittest
from tools.ui_generator import UIGenerator

class TestUIGenerator(unittest.TestCase):
    def test_ui_generator(self):
        generator = UIGenerator()
        self.assertIsNotNone(generator)
        # We can't easily test generation without a full project structure,
        # but we can test initialization.

if __name__ == '__main__':
    unittest.main()
