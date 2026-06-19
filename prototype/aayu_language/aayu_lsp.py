import sys
import json
import logging
from lexer import Lexer
from parser import Parser
from errors import AayuSyntaxError

# Set up logging to a file so it doesn't corrupt stdout (which is used for LSP)
logging.basicConfig(filename='aayu_lsp.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('aayu_lsp')

class AayuLanguageServer:
    def __init__(self):
        self.documents = {}

    def read_message(self):
        # Read Content-Length: ...\r\n\r\n
        line = sys.stdin.readline()
        if not line:
            return None
            
        if not line.startswith("Content-Length: "):
            return None
            
        content_length = int(line.split(":")[1].strip())
        
        # Read the blank line
        sys.stdin.readline()
        
        # Read the body
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
                    "textDocumentSync": 1, # Full sync
                    "completionProvider": {
                        "resolveProvider": False
                    }
                }
            }
        }

    def validate_document(self, uri, text):
        logger.info(f"Validating document {uri}")
        diagnostics = []
        
        try:
            lexer = Lexer(text)
            tokens = lexer.tokenize()
            parser = Parser(tokens, filename=uri)
            parser.parse()
        except AayuSyntaxError as e:
            # LSP uses 0-indexed positions
            line = max(0, e.line - 1)
            col = max(0, e.column - 1)
            
            diagnostic = {
                "range": {
                    "start": {"line": line, "character": col},
                    "end": {"line": line, "character": col + 10} # Highlight a bit of text
                },
                "severity": 1, # Error
                "message": e.message,
                "source": "aayu"
            }
            diagnostics.append(diagnostic)
        except Exception as e:
            logger.error(f"Unknown parsing error: {str(e)}")
            
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
        logger.info("Providing completions")
        
        keywords = ["number", "text", "is", "show", "if", "else", "while", "end", 
                   "task", "run", "with", "and", "list", "add", "to", "for", "each", 
                   "in", "return", "use", "export", "map", "set", "get", "from", "serve", "on", "route", "render", "form"]
                   
        builtins = ["upper", "lower", "length", "sqrt", "abs", "round", "random_number"]
        
        items = []
        for kw in keywords:
            items.append({
                "label": kw,
                "kind": 14, # Keyword
                "detail": "Aayu Keyword"
            })
            
        for bi in builtins:
            items.append({
                "label": bi,
                "kind": 3, # Function
                "detail": "Aayu Built-in Function"
            })
            
        return {
            "jsonrpc": "2.0",
            "id": request.get("id"),
            "result": items
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
                    
                elif method == "shutdown":
                    self.send_message({
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "result": None
                    })
                    
                elif method == "exit":
                    break
                    
            except Exception as e:
                logger.error(f"Error handling message: {str(e)}", exc_info=True)

if __name__ == "__main__":
    server = AayuLanguageServer()
    server.run()
