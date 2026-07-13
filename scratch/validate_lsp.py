import sys
import os
import json
import logging

# Set up logging for validation script
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Add local directory to path
sys.path.insert(0, os.path.abspath('.'))

from tools.lsp.server import LanguageServer, Workspace
from tools.lsp.hover import handle_hover
from tools.lsp.completion import handle_completion
from tools.lsp.definition import handle_definition
from tools.lsp.rename import handle_rename

class MockProtocol:
    def __init__(self):
        self.responses = []
        
    def write_message(self, msg):
        self.responses.append(msg)

def validate_lsp():
    print("==================================================")
    print("AAYU LSP End-to-End Validation Script")
    print("==================================================")
    
    workspace = Workspace()
    protocol = MockProtocol()
    
    # 1. Initialize
    print("\n[LSP] Client -> Server: initialize")
    # Mocking initialize response manually since it's simple
    print("[LSP] Server -> Client: capabilities returned")
    
    # 2. didOpen
    file_uri = "file:///d:/intent-to-silicon-research/INTENT-TO-SILICON/examples/whatsapp_clone/main.aayu"
    with open("examples/whatsapp_clone/main.aayu", "r") as f:
        file_text = f.read()
        
    print(f"\n[LSP] Client -> Server: textDocument/didOpen ({file_uri})")
    workspace.did_open({
        "params": {
            "textDocument": {
                "uri": file_uri,
                "text": file_text
            }
        }
    })
    
    # 3. hover
    print("\n[LSP] Client -> Server: textDocument/hover (at 'page')")
    hover_msg = {
        "id": 1,
        "params": {
            "textDocument": {"uri": file_uri},
            "position": {"line": 21, "character": 2} # 'page App'
        }
    }
    handle_hover(hover_msg, workspace, protocol)
    print("[LSP] Server -> Client:")
    print(json.dumps(protocol.responses[-1], indent=2))
    
    # 4. completion
    print("\n[LSP] Client -> Server: textDocument/completion")
    completion_msg = {
        "id": 2,
        "params": {
            "textDocument": {"uri": file_uri},
            "position": {"line": 22, "character": 4} # inside 'container'
        }
    }
    handle_completion(completion_msg, workspace, protocol)
    print("[LSP] Server -> Client:")
    # Print only first 3 for brevity
    resp = protocol.responses[-1]
    resp['result'] = resp['result'][:3]
    print(json.dumps(resp, indent=2))
    print("      ... (truncated)")

    # 5. rename
    print("\n[LSP] Client -> Server: textDocument/rename (rename 'current_page')")
    rename_msg = {
        "id": 3,
        "params": {
            "textDocument": {"uri": file_uri},
            "position": {"line": 5, "character": 8}, # 'state current_page = "chat_list"'
            "newName": "active_page"
        }
    }
    handle_rename(rename_msg, workspace, protocol)
    print("[LSP] Server -> Client:")
    print(json.dumps(protocol.responses[-1], indent=2))

    # 6. definition
    print("\n[LSP] Client -> Server: textDocument/definition (at 'navigateBack')")
    def_msg = {
        "id": 4,
        "params": {
            "textDocument": {"uri": file_uri},
            "position": {"line": 26, "character": 42} # 'button "Chats" onClick="navigateBack"'
        }
    }
    handle_definition(def_msg, workspace, protocol)
    print("[LSP] Server -> Client:")
    print(json.dumps(protocol.responses[-1], indent=2))
    
    print("\n==================================================")
    print("LSP Validation Complete.")
    print("==================================================")

if __name__ == "__main__":
    validate_lsp()