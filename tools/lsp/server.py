import sys
import json
import logging
from .protocol import LSPProtocol
from .workspace import Workspace
from .cancellation import CancellationManager

logging.basicConfig(filename="aayu_lsp.log", level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AAYU_LSP")

class LanguageServer:
    def __init__(self):
        self.protocol = LSPProtocol(sys.stdin, sys.stdout)
        self.workspace = Workspace()
        self.cancellation = CancellationManager()

    def start(self):
        logger.info("Starting AAYU LSP Server")
        while True:
            try:
                msg = self.protocol.read_message()
                if not msg:
                    break
                    
                self.dispatch(msg)
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    def dispatch(self, msg):
        method = msg.get("method")
        
        # Dispatch to appropriate handlers based on method
        if method == "initialize":
            self.handle_initialize(msg)
        elif method == "textDocument/didOpen":
            self.workspace.did_open(msg)
            self._trigger_diagnostics(msg)
        elif method == "textDocument/didChange":
            self.workspace.did_change(msg)
            self._trigger_diagnostics(msg)
        elif method == "textDocument/hover":
            from .hover import handle_hover
            handle_hover(msg, self.workspace, self.protocol)
        elif method == "textDocument/definition":
            from .definition import handle_definition
            handle_definition(msg, self.workspace, self.protocol)
        elif method == "textDocument/completion":
            from .completion import handle_completion
            handle_completion(msg, self.workspace, self.protocol)
        elif method == "textDocument/references":
            self.protocol.write_message({"jsonrpc": "2.0", "id": msg.get("id"), "result": []})
        elif method == "textDocument/rename":
            from .rename import handle_rename
            handle_rename(msg, self.workspace, self.protocol)
        elif method == "textDocument/formatting":
            from .formatting import handle_formatting
            handle_formatting(msg, self.workspace, self.protocol)
        elif method == "workspace/symbol":
            from .symbols import handle_workspace_symbol
            handle_workspace_symbol(msg, self.workspace, self.protocol)
        elif method == "textDocument/codeAction":
            from .code_actions import handle_code_action
            handle_code_action(msg, self.workspace, self.protocol)
        elif method == "$/cancelRequest":
            self.cancellation.cancel(msg.get("params", {}).get("id"))
        elif method == "shutdown":
            self.protocol.write_message({"jsonrpc": "2.0", "id": msg.get("id"), "result": None})
        elif method == "exit":
            sys.exit(0)

    def handle_initialize(self, msg):
        response = {
            "jsonrpc": "2.0",
            "id": msg["id"],
            "result": {
                "capabilities": {
                    "textDocumentSync": 1, # Full sync (for now, will move to Incremental (2))
                    "hoverProvider": True,
                    "definitionProvider": True,
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": ["."]
                    },
                    "referencesProvider": True,
                    "renameProvider": True,
                    "documentFormattingProvider": True,
                    "workspaceSymbolProvider": True,
                    "codeActionProvider": True,
                    "diagnosticProvider": {
                        "interFileDependencies": False,
                        "workspaceDiagnostics": False
                    }
                },
                "serverInfo": {
                    "name": "aayu-lsp",
                    "version": "1.1.0"
                }
            }
        }
        self.protocol.write_message(response)
        logger.info("Initialized successfully")

    def _trigger_diagnostics(self, msg):
        uri = msg["params"]["textDocument"]["uri"]
        doc = self.workspace.get_document(uri)
        
        from .diagnostics import generate_diagnostics
        diagnostics = generate_diagnostics(doc)
        
        self.protocol.write_message({
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics
            }
        })
