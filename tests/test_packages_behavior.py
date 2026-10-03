import unittest
import os
import sys
import io

from tests.compiler.test_helpers import CompilerE2EMixin

class TestPackagesBehavior(CompilerE2EMixin, unittest.TestCase):
    def get_package_code(self, pkg_name):
        path = f"official_packages/{pkg_name}/main.aayu"
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
            # Strip the app declaration so it acts as a normal script
            return "\n".join([line for line in code.split("\n") if not line.startswith("app ")])

    def test_aayu_math(self):
        pkg = self.get_package_code("aayu-math")
        test_code = pkg + """
let res1 = add(5, 10)
let res2 = abs(0 - 5)
print("RES1=" + res1)
print("RES2=" + res2)
"""
        output = self.execute_aayu(test_code)
        self.assertIn("RES1=15", output)
        self.assertIn("RES2=5", output)

    def test_aayu_http(self):
        pkg = self.get_package_code("aayu-http")
        test_code = pkg + """
print("tested http!!!")
"""
        output = self.execute_aayu(test_code)
        self.assertIn("tested http!!!", output)
        
    def test_aayu_gemini(self):
        pkg = self.get_package_code("aayu-gemini")
        test_code = pkg + """
let res = generateContent("hello")
print("GEMINI_RESPONSE=" + res)
"""
        output = self.execute_aayu(test_code)
        output_str = "\n".join(output)
        self.assertTrue("Hello" in output_str or "AI" in output_str or "hello" in output_str.lower())

if __name__ == '__main__':
    unittest.main()
