import unittest
import os
import tempfile
from tools.formatter import AAYUFormatter
from tools.linter import AAYULinter
from tools.aayu_lsp import AayuLanguageServer

class TestTools(unittest.TestCase):
    def test_formatter_various(self):
        source = """
        project Test.
        task main.
        let x: Int = 1.
        let y: String = "test".
        let b: Boolean = true.
        let l: List = [1, 2, 3].
        let m: Map = {"a": 1, "b": 2}.
        if x > 0.
        print("x is positive").
        else.
        print("x is negative or zero").
        end.
        while x < 10.
        x = x + 1.
        end.
        end.
        run main.
        """
        formatter = AAYUFormatter(source)
        fmt = formatter.format()
        self.assertIn("project Test.", fmt)
        self.assertIn("task main.", fmt)
        
    def test_linter_various(self):
        source = """
        project Test.
        task main.
        let x: Int = 1.
        x = 2.
        end.
        run main.
        """
        with tempfile.NamedTemporaryFile('w', delete=False, suffix='.aayu') as f:
            f.write(source)
            f.flush()
            linter = AAYULinter(f.name)
            issues = linter.lint()
        os.remove(f.name)
        self.assertIsInstance(issues, list)
        
    def test_lsp(self):
        server = AayuLanguageServer()
        msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {}
        }
        res = server.handle_message(msg)
        self.assertIn("capabilities", res.get("result", {}))

if __name__ == '__main__':
    unittest.main()
