"""
=============================================================================
FILE: aayu_lsp.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import sys
import json
import logging
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.ast_nodes import RecordDeclarationNode, EntityDeclarationNode, TaskNode
from compiler.frontend.errors import AAYUSyntaxError

# Set up logging to a file so it doesn't corrupt stdout (which is used for LSP)
logging.basicConfig(filename='aayu_lsp.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('aayu_lsp')

class AayuLanguageServer:
    def __init__(self):
        self.documents = {}
        # Simple symbol table for the AST
        self.entities = {} # name -> Node

    def read_message(self):
        line = sys.stdin.readline()
        if not line:
            return None
        if not line.startswith("Content-Length: "):
            return None
            
        content_length = int(line.split(":")[1].strip())
        sys.stdin.readline() # blank line
        body = sys.stdin.read(content_length)
        return json.loads(body)

    def send_message(self, message):
        body = json.dumps(message, separators=(',', ':'))
        response = f"Content-Length: {len(body)}\r\n\r\n{body}"
        sys.stdout.write(response)
        sys.stdout.flush()

    def handle_initialize(self, request):
        logger.info("Initializing server")
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": {
                "capabilities": {
                    "textDocumentSync": 1,
                    "completionProvider": {
                        "resolveProvider": False,
                        "triggerCharacters": ["."]
                    },
                    "hoverProvider": True
                }
            }
        }

    def validate_document(self, uri, text):
        logger.info(f"Validating document {uri}")
        diagnostics = []
        self.entities.clear()
        
        ast_nodes = []
        
        try:
            import os
            import sys
            cli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, cli_dir)
            
            from engine.api import AAYUEngine
            engine = AAYUEngine()
            project = engine.load_source(text)
            ast = project.validate()
            ast_nodes = ast.statements
        except AAYUSyntaxError as e:
            line = max(0, e.line - 1)
            col = max(0, e.column - 1)
            diagnostics.append({
                "range": {
                    "start": {"line": line, "character": col},
                    "end": {"line": line, "character": col + 10}
                },
                "severity": 1,
                "message": e.message,
                "source": "aayu/syntax"
            })
            # Best effort semantic analysis on partial tokens if parser threw
            # We will just ignore for now since parser stops on first error
        except Exception as e:
            logger.error(f"Unknown parsing error: {str(e)}")

        # Semantic Diagnostics: Duplicate Records
        seen = set()
        for node in ast_nodes:
            if isinstance(node, (RecordDeclarationNode, EntityDeclarationNode)):
                name = node.name
                if name in seen:
                    diagnostics.append({
                        "range": {
                            # We don't have token lines on the AST node currently, so we put it at top of file
                            "start": {"line": 0, "character": 0},
                            "end": {"line": 0, "character": 10}
                        },
                        "severity": 1,
                        "message": f"Duplicate Record/Entity defined: '{name}'",
                        "source": "aayu/semantic"
                    })
                seen.add(name)
                self.entities[name] = node
            elif isinstance(node, TaskNode):
                self.entities[node.name] = node

        # Send diagnostics notification
        self.send_message({
            "jsonrpc": "2.0",
            "method": "textDocument/publishDiagnostics",
            "params": {
                "uri": uri,
                "diagnostics": diagnostics
            }
        })

    def get_completions(self, request):
        params = request.get("params", {})
        pos = params.get("position", {})
        uri = params.get("textDocument", {}).get("uri", "")
        text = self.documents.get(uri, "")
        
        lines = text.split('\n')
        line = lines[pos.get("line", 0)]
        prefix = line[:pos.get("character", 0)]
        
        items = []
        
        # AST-Driven completion: If user types "Entity.", suggest fields
        if prefix.endswith("."):
            entity_name = prefix[:-1].split()[-1] # very naive extraction of the word before .
            if entity_name in self.entities:
                node = self.entities[entity_name]
                if hasattr(node, 'fields'):
                    for field in node.fields:
                        items.append({
                            "label": field,
                            "kind": 5, # Field
                            "detail": f"Field of {entity_name}"
                        })
                    return {"jsonrpc": "2.0", "id": request.get("id"), "result": items}

        keywords = ["record", "system", "task", "page", "entity", "workflow", "use", "if", "else", "end", "run"]
        for kw in keywords:
            items.append({
                "label": kw,
                "kind": 14, # Keyword
                "detail": "Aayu Keyword"
            })
            
        for entity_name in self.entities:
            items.append({
                "label": entity_name,
                "kind": 7, # Class
                "detail": "Defined Entity/Task"
            })
            
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": items
        }

    def get_hover(self, request):
        params = request.get("params", {})
        pos = params.get("position", {})
        uri = params.get("textDocument", {}).get("uri", "")
        text = self.documents.get(uri, "")
        
        lines = text.split('\n')
        line = lines[pos.get("line", 0)]
        
        # Very naive word extraction around cursor
        import re
        words = re.finditer(r'[A-Za-z_][A-Za-z0-9_]*', line)
        hover_word = None
        for w in words:
            if w.start() <= pos.get("character", 0) <= w.end():
                hover_word = w.group(0)
                break
                
        if hover_word and hover_word in self.entities:
            node = self.entities[hover_word]
            if isinstance(node, (RecordDeclarationNode, EntityDeclarationNode)):
                fields_str = ", ".join(node.fields)
                markdown = f"**Record `{hover_word}`**\n\nFields: {fields_str}"
            elif isinstance(node, TaskNode):
                markdown = f"**Task `{hover_word}`**"
            else:
                markdown = f"`{hover_word}`"
                
            return {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "contents": {
                        "kind": "markdown",
                        "value": markdown
                    }
                }
            }
            
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": None
        }

    def run(self):
        logger.info("Aayu Language Server Started")
        while True:
            try:
                message = self.read_message()
                if message is None:
                    break
                    
                method = message.get("method")
                logger.info(f"Received method: {method}")
                
                if method == "initialize":
                    self.send_message(self.handle_initialize(message))
                elif method == "textDocument/didOpen":
                    uri = message["params"]["textDocument"]["uri"]
                    text = message["params"]["textDocument"]["text"]
                    self.documents[uri] = text
                    self.validate_document(uri, text)
                elif method == "textDocument/didChange":
                    uri = message["params"]["textDocument"]["uri"]
                    text = message["params"]["contentChanges"][0]["text"]
                    self.documents[uri] = text
                    self.validate_document(uri, text)
                elif method == "textDocument/completion":
                    self.send_message(self.get_completions(message))
                elif method == "textDocument/hover":
                    self.send_message(self.get_hover(message))
                elif method == "shutdown":
                    self.send_message({"jsonrpc": "2.0", "id": message.get("id"), "result": None})
                elif method == "exit":
                    break
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}", exc_info=True)

if __name__ == "__main__":
    server = AayuLanguageServer()
    server.run()

