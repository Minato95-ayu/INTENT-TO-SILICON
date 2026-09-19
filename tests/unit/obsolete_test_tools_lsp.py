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
