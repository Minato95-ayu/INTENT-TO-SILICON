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
from tests.compiler.test_helpers import CompilerE2EMixin

class TestExceptions(CompilerE2EMixin, unittest.TestCase):
    def test_basic_throw_catch(self):
        code = """
        let result = "none"
        try
            throw "something went wrong"
            result = "unreachable"
        catch (e)
            result = "caught"
        end
        print(result)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("caught", out)

    def test_catch_binding(self):
        code = """
        try
            throw "my error message"
        catch (e)
            print(e)
        end
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertTrue(any("my error message" in o for o in out))
        
    def test_normal_flow_no_catch(self):
        code = """
        try
            print("normal")
        catch (e)
            print("caught")
        end
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("normal", out)
        self.assertNotIn("caught", out)

if __name__ == '__main__':
    unittest.main()
