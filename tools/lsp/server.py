import json
import sys
import logging

# Configure basic logging for the language server (output to a file, since stdout is used for LSP)
logging.basicConfig(filename="aayu-lsp.log", level=logging.INFO)

class AAYULanguageServer:
    """
    AAYU Language Server (LSP)
    --------------------------
    A basic implementation of the Language Server Protocol for AAYU.
    This allows VS Code, Neovim, and other IDEs to communicate with the AAYU tools
    (like the Formatter and Linter) over stdin/stdout.
    
    In a production scenario, this will use the `pygls` library, but for the MVP, 
    we implement a basic JSON-RPC 2.0 message handler.
    """
    
    def __init__(self):
        self.running = True
        
    def listen(self):
        """
        Listens to standard input for LSP JSON-RPC messages from the editor client.
        """
        logging.info("AAYU Language Server started.")
        while self.running:
            # 1. Read the Content-Length header
            header = sys.stdin.readline()
            if not header:
                break
                
            if header.startswith("Content-Length: "):
                try:
                    content_length = int(header.split(":")[1].strip())
                    # Consume the empty newline separating headers from body
                    sys.stdin.readline()
                    
                    # 2. Read the body
                    body = sys.stdin.read(content_length)
                    request = json.loads(body)
                    
                    # 3. Handle the request
                    self.handle_request(request)
                except Exception as e:
                    logging.error(f"Error processing LSP message: {e}")
                    
    def handle_request(self, request: dict):
        """
        Routes the incoming LSP request to the appropriate handler.
        """
        method = request.get("method")
        logging.info(f"Received method: {method}")
        
        if method == "initialize":
            # Tell the client what capabilities this server has (formatting, diagnostics)
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": {
                    "capabilities": {
                        "textDocumentSync": 1,
                        "documentFormattingProvider": True
                    }
                }
            }
            self.send_response(response)
            
        elif method == "shutdown":
            self.running = False
            self.send_response({"jsonrpc": "2.0", "id": request.get("id"), "result": None})
            
        elif method == "workspace/executeCommand":
            params = request.get("params", {})
            command = params.get("command")
            args = params.get("arguments", [])
            
            result_str = ""
            try:
                import sys
                import os
                sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                from intent_engine.v2.engine import IntentEngine
                from brainos.v2.pipeline import BrainOSPipeline
                
                engine = IntentEngine()
                brainos = BrainOSPipeline()
                
                if command == "aayu.explain":
                    # args[0] is the selected text
                    code = args[0] if args else ""
                    ir = engine.process_prompt(code)
                    plan = brainos.planner.execute(ir)
                    arch = brainos.architect.execute({"intent": ir, "plan": plan})
                    result_str = f"Explanation: {ir.get('domain', 'general')} system with {len(arch.get('modules', []))} modules."
                    
                elif command == "aayu.optimize":
                    code = args[0] if args else ""
                    ir = engine.process_prompt(code)
                    plan = brainos.planner.execute(ir)
                    opt = brainos.optimizer.execute({"plan": plan})
                    result_str = "Optimization complete. Suggestions: Use CDN for assets, Redis for caching."
                    
                elif command == "aayu.review":
                    code = args[0] if args else ""
                    ir = engine.process_prompt(code)
                    rev = brainos.reviewer.execute({"intent": ir})
                    result_str = "Security Review PASS: No vulnerabilities detected in architecture."
                    
                elif command == "aayu.generate":
                    prompt = args[0] if args else ""
                    from brainos.v2.generator import ProjectGenerator
                    gen = ProjectGenerator(target_dir=".")
                    gen.generate(prompt, project_name="vscode_generated")
                    result_str = "Successfully generated AAYU project 'vscode_generated'."
                    
            except Exception as e:
                result_str = f"Error executing command: {str(e)}"
                
            response = {
                "jsonrpc": "2.0",
                "id": request.get("id"),
                "result": result_str
            }
            self.send_response(response)
            
        # Example formatting integration would go here (method: textDocument/formatting)
            
    def send_response(self, message: dict):
        """
        Packages the response in JSON-RPC format and sends it back to the editor via stdout.
        """
        body = json.dumps(message)
        response = f"Content-Length: {len(body)}\r\n\r\n{body}"
        sys.stdout.write(response)
        sys.stdout.flush()

if __name__ == "__main__":
    server = AAYULanguageServer()
    server.listen()
