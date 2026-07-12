import unittest
from typing import Any, Dict
from runtime.kernel.core import RuntimeKernel
from runtime.plugins.theme.runtime import ThemeRuntime

class TestThemeRuntime(unittest.TestCase):
    def setUp(self):
        self.kernel = RuntimeKernel()
        self.theme = ThemeRuntime()
        self.kernel.registry.register(self.theme)
        self.kernel.boot()

    def tearDown(self):
        self.kernel.shutdown()

    def test_default_theme_mode(self):
        res = self.kernel.dispatch("theme", "get_mode", {})
        self.assertTrue(res.success)
        self.assertEqual(res.data["mode"], "light")

    def test_switch_theme_mode(self):
        self.kernel.dispatch("theme", "set_mode", {"mode": "dark"})
        res = self.kernel.dispatch("theme", "get_mode", {})
        self.assertEqual(res.data["mode"], "dark")

    def test_get_color_palette(self):
        res = self.kernel.dispatch("theme", "get_colors", {})
        self.assertTrue(res.success)
        self.assertIn("primary", res.data["colors"])
        self.assertIn("background", res.data["colors"])
        self.assertIn("text", res.data["colors"])
        
        # Test dark mode colors change
        self.kernel.dispatch("theme", "set_mode", {"mode": "dark"})
        dark_res = self.kernel.dispatch("theme", "get_colors", {})
        self.assertNotEqual(res.data["colors"]["background"], dark_res.data["colors"]["background"])

    def test_get_spacing(self):
        res = self.kernel.dispatch("theme", "get_spacing", {})
        self.assertTrue(res.success)
        self.assertEqual(res.data["spacing"]["sm"], 4)
        self.assertEqual(res.data["spacing"]["md"], 8)
        self.assertEqual(res.data["spacing"]["lg"], 16)

    def test_get_typography(self):
        res = self.kernel.dispatch("theme", "get_typography", {})
        self.assertTrue(res.success)
        self.assertIn("h1", res.data["typography"])
        self.assertIn("body", res.data["typography"])

if __name__ == '__main__':
    unittest.main()
