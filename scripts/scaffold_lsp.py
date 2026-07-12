import os

lsp_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tools\lsp"
os.makedirs(lsp_dir, exist_ok=True)

with open(os.path.join(lsp_dir, 'language_server.py'), 'w', encoding='utf-8') as f:
    f.write('''\
import json
import sys

class LanguageServer:
    def __init__(self):
        self.documents = {}
        
    def handle_request(self, request):
        if request.get("method") == "initialize":
            return {"capabilities": {"textDocumentSync": 1, "completionProvider": {}, "hoverProvider": True, "definitionProvider": True, "referencesProvider": True, "documentFormattingProvider": True, "renameProvider": True}}
        elif request.get("method") == "textDocument/didOpen":
            self.documents[request["params"]["textDocument"]["uri"]] = request["params"]["textDocument"]["text"]
        elif request.get("method") == "textDocument/completion":
            return [{"label": "print", "kind": 3}, {"label": "show", "kind": 3}]
        elif request.get("method") == "textDocument/hover":
            return {"contents": "AAYU Keyword"}
        elif request.get("method") == "textDocument/formatting":
            return [] # Mock formatting response
        return None

    def start(self):
        while True:
            line = sys.stdin.readline()
            if not line: break
            try:
                req = json.loads(line)
                res = self.handle_request(req)
                if res:
                    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": req.get("id"), "result": res}) + "\\n")
                    sys.stdout.flush()
            except:
                pass
'''
    )

print("Created LSP mock")
