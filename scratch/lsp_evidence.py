import sys
import os
import json

# Add local directory to path
sys.path.insert(0, os.path.abspath('.'))

from tools.lsp.hover import handle_hover
from tools.lsp.server import Workspace

class MockProtocol:
    def write_message(self, msg):
        print(json.dumps(msg, indent=2))

workspace = Workspace()
msg_open = {
    "method": "textDocument/didOpen",
    "params": {
        "textDocument": {
            "uri": "file:///main.aayu",
            "text": "page Home\n  text \"Hello\"\nend\n"
        }
    }
}
workspace.did_open(msg_open)
doc = workspace.get_document("file:///main.aayu")

msg_hover = {
    "id": 1,
    "params": {
        "textDocument": {"uri": "file:///main.aayu"},
        "position": {"line": 0, "character": 2}
    }
}
protocol = MockProtocol()
print("--- HOVER EVIDENCE ---")
handle_hover(msg_hover, workspace, protocol)

from tools.lsp.completion import handle_completion
print("--- COMPLETION EVIDENCE ---")
handle_completion(msg_hover, workspace, protocol)

from tools.lsp.diagnostics import generate_diagnostics
print("--- DIAGNOSTICS EVIDENCE ---")
diagnostics = generate_diagnostics(doc)
protocol.write_message({
    "jsonrpc": "2.0",
    "method": "textDocument/publishDiagnostics",
    "params": {
        "uri": "file:///main.aayu",
        "diagnostics": diagnostics
    }
})
