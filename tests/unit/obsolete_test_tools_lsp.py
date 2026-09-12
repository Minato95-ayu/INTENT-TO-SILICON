import unittest
from tools.aayu_lsp import AayuLanguageServer
import io

class TestAAYULSP(unittest.TestCase):
    def test_lsp_init(self):
        server = AayuLanguageServer()
        self.assertIsNotNone(server)
        
        # Test basic message handling dummy
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
