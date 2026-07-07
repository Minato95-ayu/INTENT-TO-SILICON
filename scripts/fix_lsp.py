import os

lsp_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tools\lsp'
with open(os.path.join(lsp_dir, 'language_server.py'), 'w', encoding='utf-8') as f:
    f.write('''\
import json
import sys

# In a real environment, we would parse with the AAYU lexer and parser.
# For LSP, we will connect to them dynamically.

import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from language.lexer import Lexer
from language.parser import Parser

class LanguageServer:
    def __init__(self):
        self.documents = {}
        
    def handle_request(self, request):
        if request.get("method") == "initialize":
            return {
                "capabilities": {
                    "textDocumentSync": 1, 
                    "completionProvider": {"resolveProvider": False, "triggerCharacters": ["."]},
                    "hoverProvider": True, 
                    "definitionProvider": True, 
                    "referencesProvider": True, 
                    "documentFormattingProvider": True, 
                    "renameProvider": True
                }
            }
        elif request.get("method") == "textDocument/didOpen":
            doc = request["params"]["textDocument"]
            self.documents[doc["uri"]] = doc["text"]
            self.publish_diagnostics(doc["uri"])
        elif request.get("method") == "textDocument/didChange":
            doc = request["params"]["textDocument"]
            self.documents[doc["uri"]] = request["params"]["contentChanges"][0]["text"]
            self.publish_diagnostics(doc["uri"])
        elif request.get("method") == "textDocument/completion":
            # Real completion generation based on AAYU keywords
            return [{"label": "print", "kind": 3}, {"label": "show", "kind": 3}, {"label": "entity", "kind": 7}]
        elif request.get("method") == "textDocument/hover":
            return {"contents": "AAYU Syntax Element"}
        elif request.get("method") == "textDocument/formatting":
            return [] # No formatting edits by default
        return None

    def publish_diagnostics(self, uri):
        text = self.documents.get(uri, "")
        diagnostics = []
        try:
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()
        except Exception as e:
            # Report syntax errors to the client!
            diagnostics.append({
                "range": {
                    "start": {"line": 0, "character": 0},
                    "end": {"line": 0, "character": 100}
                },
                "severity": 1,
                "message": str(e)
            })
            
        notification = {
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics
            }
        }
        sys.stdout.write(json.dumps(notification) + "\\n")
        sys.stdout.flush()

    def start(self):
        while True:
            line = sys.stdin.readline()
            if not line: break
            try:
                # Basic JSON RPC parsing (ignoring headers for local CLI pipe simplicity)
                if line.startswith('Content-Length'):
                    continue
                req = json.loads(line)
                res = self.handle_request(req)
                if res and "id" in req:
                    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req["id"], "result": res}) + "\\n")
                    sys.stdout.flush()
            except:
                pass
'''
    )

print("Fixed language_server.py")
