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
