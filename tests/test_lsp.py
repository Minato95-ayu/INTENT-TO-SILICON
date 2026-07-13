import pytest
import io
import json
from tools.lsp.server import LanguageServer
from tools.lsp.protocol import LSPProtocol

class MockProtocol(LSPProtocol):
    def __init__(self):
        self.output = []
        
    def write_message(self, message):
        self.output.append(message)
        
    def read_message(self):
        # We manually drive this in tests
        pass

def test_lsp_diagnostics():
    server = LanguageServer()
    server.protocol = MockProtocol()
    
    # 1. Initialize
    server.dispatch({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize"
    })
    assert len(server.protocol.output) == 1
    assert "capabilities" in server.protocol.output[0]["result"]
    server.protocol.output.clear()
    
    # 2. Open File with Syntax Error (missing identifier after page)
    server.dispatch({
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": "file:///test.aayu",
                "text": "page {\n}",
                "version": 1
            }
        }
    })
    
    # Should publish diagnostics
    assert len(server.protocol.output) == 1
    notification = server.protocol.output[0]
    assert notification["method"] == "textDocument/publishDiagnostics"
    diagnostics = notification["params"]["diagnostics"]
    
    # There should be an error because `page {` is invalid (missing identifier)
    assert len(diagnostics) > 0
    assert diagnostics[0]["severity"] == 1
    
    server.protocol.output.clear()
    
    # 3. Change to valid code
    server.dispatch({
        "jsonrpc": "2.0",
        "method": "textDocument/didChange",
        "params": {
            "textDocument": {
                "uri": "file:///test.aayu",
                "version": 2
            },
            "contentChanges": [
                {"text": "page Home\nend"}
            ]
        }
    })
    
    notification = server.protocol.output[0]
    diagnostics = notification["params"]["diagnostics"]
    # Errors should be cleared
    assert len(diagnostics) == 0

def test_lsp_completion():
    server = LanguageServer()
    server.protocol = MockProtocol()
    
    server.dispatch({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/completion",
        "params": {
            "textDocument": {"uri": "file:///test.aayu"},
            "position": {"line": 0, "character": 0}
        }
    })
    
    assert len(server.protocol.output) == 1
    response = server.protocol.output[0]
    assert response["id"] == 2
    items = response["result"]
    assert len(items) > 0
    
if __name__ == '__main__':
    pytest.main(['-v', __file__])
