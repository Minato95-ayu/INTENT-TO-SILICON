import sys
import json
import logging
from lexer import Lexer
from parser import Parser
from errors import AAYUError

# We log to a file so it doesn't corrupt stdout which is used for LSP
logging.basicConfig(filename="aayu_lsp.log", level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def read_message():
    content_length = 0
    while True:
        line = sys.stdin.readline()
        if not line:
            return None
        line = line.strip()
        if not line:
            break
        if line.startswith("Content-Length:"):
            content_length = int(line.split(":")[1].strip())
    
    if content_length == 0:
        return None
        
    content = sys.stdin.read(content_length)
    return json.loads(content)

def write_message(msg_dict):
    msg_str = json.dumps(msg_dict)
    content_length = len(msg_str.encode("utf-8"))
    sys.stdout.write(f"Content-Length: {content_length}\r\n\r\n{msg_str}")
    sys.stdout.flush()

def handle_did_change(params):
    uri = params["textDocument"]["uri"]
    text = params["contentChanges"][0]["text"]
    diagnostics = run_diagnostics(text)
    
    write_message({
        "jsonrpc": "2.0",
        "method": "textDocument/publishDiagnostics",
        "params": {
            "uri": uri,
            "diagnostics": diagnostics
        }
    })

def handle_did_open(params):
    uri = params["textDocument"]["uri"]
    text = params["textDocument"]["text"]
    diagnostics = run_diagnostics(text)
    
    write_message({
        "jsonrpc": "2.0",
        "method": "textDocument/publishDiagnostics",
        "params": {
            "uri": uri,
            "diagnostics": diagnostics
        }
    })

def run_diagnostics(code):
    diagnostics = []
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        # For now, we only catch Syntax Errors in live editor since full semantic checks require running
    except AAYUError as e:
        error_data = e.to_dict()
        line_idx = error_data["line"] - 1
        diagnostics.append({
            "range": {
                "start": {"line": line_idx, "character": 0},
                "end": {"line": line_idx, "character": 100}
            },
            "severity": 1, # Error
            "source": "aayu",
            "message": f"{error_data['message']}\nHint: {error_data['hint']}"
        })
    except Exception as e:
        pass # Ignore generic python crashes for diagnostics
    return diagnostics

def handle_completion(msg_id, params):
    # Snippet completion and keyword completion
    items = [
        {
            "label": "task",
            "kind": 14, # Snippet
            "insertText": "task ${1:name} with ${2:req}.\n\t$0\nend.",
            "insertTextFormat": 2 # Snippet
        },
        {
            "label": "entity",
            "kind": 14,
            "insertText": "entity ${1:Name}.\n\ttext ${2:field}.\nend.",
            "insertTextFormat": 2
        },
        {
            "label": "route",
            "kind": 14,
            "insertText": "route \"${1:/path}\" to ${2:task_name}.",
            "insertTextFormat": 2
        },
        {
            "label": "show",
            "kind": 14,
            "insertText": "show ${1:value}.",
            "insertTextFormat": 2
        },
        {
            "label": "test",
            "kind": 14,
            "insertText": "test \"${1:Test Name}\".\n\t$0\nend.",
            "insertTextFormat": 2
        },
        {
            "label": "expect",
            "kind": 14,
            "insertText": "expect ${1:actual} equals ${2:expected}.",
            "insertTextFormat": 2
        },
        {
            "label": "use",
            "kind": 14,
            "insertText": "use ${1:module}.",
            "insertTextFormat": 2
        }
    ]
    
    keywords = ["number", "text", "is", "if", "else", "end", "greater", "less", "equal", "than", "to", "repeat", "times", "run", "with", "and", "list", "for", "each", "in", "return", "record", "of", "read", "write", "try", "catch", "add", "map", "set", "get", "from", "export", "serve", "on", "render", "form", "json", "create", "find", "where", "update", "delete", "login", "logout", "guard", "session", "account"]
    
    for kw in keywords:
        items.append({
            "label": kw,
            "kind": 14, # Keyword
        })
        
    write_message({
        "jsonrpc": "2.0",
        "id": msg_id,
        "result": items
    })

def main():
    logging.info("AAYU LSP Server started.")
    while True:
        try:
            msg = read_message()
            if not msg:
                break
                
            logging.debug(f"Received: {msg}")
            
            if msg.get("method") == "initialize":
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "result": {
                        "capabilities": {
                            "textDocumentSync": 1, # Full sync
                            "completionProvider": {
                                "resolveProvider": False
                            }
                        }
                    }
                })
            elif msg.get("method") == "initialized":
                pass
            elif msg.get("method") == "textDocument/didOpen":
                handle_did_open(msg.get("params"))
            elif msg.get("method") == "textDocument/didChange":
                handle_did_change(msg.get("params"))
            elif msg.get("method") == "textDocument/completion":
                handle_completion(msg.get("id"), msg.get("params"))
            elif msg.get("method") == "shutdown":
                write_message({
                    "jsonrpc": "2.0",
                    "id": msg.get("id"),
                    "result": None
                })
            elif msg.get("method") == "exit":
                break
                
        except Exception as e:
            logging.error(f"Error in LSP loop: {e}")

if __name__ == "__main__":
    main()
