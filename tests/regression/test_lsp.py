import json
import subprocess
import threading
import sys
import time

class LSPTestClient:
    def __init__(self, command=["python", "-m", "tools.cli", "lsp"]):
        self.process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0
        )
        self.message_id = 1
        self.responses = {}
        self.lock = threading.Lock()
        
        self.reader_thread = threading.Thread(target=self._read_loop, daemon=True)
        self.reader_thread.start()

    def _read_loop(self):
        while True:
            # Read header
            line = self.process.stdout.readline().decode('utf-8')
            if not line:
                break
            
            if line.startswith("Content-Length:"):
                length = int(line.split(":")[1].strip())
                # Read empty line
                self.process.stdout.readline()
                # Read content
                content = self.process.stdout.read(length).decode('utf-8')
                try:
                    data = json.loads(content)
                    if "id" in data:
                        with self.lock:
                            self.responses[data["id"]] = data
                except Exception:
                    pass

    def send_request(self, method, params):
        msg_id = self.message_id
        self.message_id += 1
        
        payload = {
            "jsonrpc": "2.0",
            "id": msg_id,
            "method": method,
            "params": params
        }
        content = json.dumps(payload)
        message = f"Content-Length: {len(content)}\r\n\r\n{content}"
        self.process.stdin.write(message.encode('utf-8'))
        self.process.stdin.flush()
        return msg_id

    def wait_for_response(self, msg_id, timeout=2.0):
        start = time.time()
        while time.time() - start < timeout:
            with self.lock:
                if msg_id in self.responses:
                    return self.responses[msg_id]
            time.sleep(0.01)
        return None

    def close(self):
        self.send_request("shutdown", {})
        time.sleep(0.1)
        self.send_request("exit", {})
        self.process.terminate()

def run_tests():
    print("Starting LSP tests...")
    client = LSPTestClient()
    
    # Test 1: Initialize
    msg_id = client.send_request("initialize", {
        "processId": None,
        "rootUri": None,
        "capabilities": {}
    })
    res = client.wait_for_response(msg_id)
    assert res is not None, "Failed to get initialize response"
    assert "capabilities" in res.get("result", {}), "No capabilities returned"
    print("✅ Initialize OK")

    # Test 2: DidOpen
    document_uri = "file:///test.aayu"
    code = "app test\nstate myVar = 10\npage Home\ntext myVar\nend"
    client.send_request("textDocument/didOpen", {
        "textDocument": {
            "uri": document_uri,
            "languageId": "aayu",
            "version": 1,
            "text": code
        }
    })
    time.sleep(0.5) # Wait for diagnostics to potentially fire
    print("✅ Document opened")

    # Test 3: Hover over `myVar`
    msg_id = client.send_request("textDocument/hover", {
        "textDocument": {"uri": document_uri},
        "position": {"line": 1, "character": 8} # On 'myVar'
    })
    res = client.wait_for_response(msg_id)
    assert res is not None, "Failed to get hover response"
    print("✅ Hover OK")

    client.close()
    print("LSP tests completed successfully.")

if __name__ == "__main__":
    run_tests()