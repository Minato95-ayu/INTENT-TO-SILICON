"""
=============================================================================
FILE: lsp_tester.py
PURPOSE: Test file - Validates system functionality
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test file - validates system functionality.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import subprocess
import threading
import time

def read_lsp_responses(process):
    while True:
        line = process.stdout.readline()
        if not line:
            break
        line = line.decode('utf-8')
        if line.startswith("Content-Length: "):
            length = int(line.split(":")[1].strip())
            process.stdout.readline() # blank line
            body = process.stdout.read(length).decode('utf-8')
            print("\n[LSP Response]")
            print(json.dumps(json.loads(body), indent=2))

def send_message(process, message):
    body = json.dumps(message, separators=(',', ':'))
    payload = f"Content-Length: {len(body)}\r\n\r\n{body}"
    process.stdin.write(payload.encode('utf-8'))
    process.stdin.flush()

if __name__ == "__main__":
    print("Starting Aayu LSP locally...")
    process = subprocess.Popen(
        ["python", "aayu_lsp.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Start a thread to read responses
    reader_thread = threading.Thread(target=read_lsp_responses, args=(process,))
    reader_thread.daemon = True
    reader_thread.start()

    # 1. Initialize
    send_message(process, {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    })
    time.sleep(1)

    # 2. Open a document with a syntax error
    print("\nSending textDocument/didOpen with broken code...")
    send_message(process, {
        "jsonrpc": "2.0",
        "method": "textDocument/didOpen",
        "params": {
            "textDocument": {
                "uri": "file:///test.aayu",
                "languageId": "aayu",
                "version": 1,
                "text": "task hello\n\nshow \"hi\"." # Missing dot after task declaration
            }
        }
    })
    time.sleep(1)

    # 3. Request Completion
    print("\nSending textDocument/completion request...")
    send_message(process, {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "textDocument/completion",
        "params": {
            "textDocument": {"uri": "file:///test.aayu"},
            "position": {"line": 2, "character": 0}
        }
    })
    time.sleep(1)

    # 4. Fix the document with didChange
    print("\nSending textDocument/didChange to fix the code...")
    send_message(process, {
        "jsonrpc": "2.0",
        "method": "textDocument/didChange",
        "params": {
            "textDocument": {"uri": "file:///test.aayu", "version": 2},
            "contentChanges": [{
                "text": "task hello.\n\nshow \"hi\"."
            }]
        }
    })
    time.sleep(1)

    # 5. Shutdown
    send_message(process, {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "shutdown",
        "params": {}
    })
    time.sleep(0.5)
    
    send_message(process, {
        "jsonrpc": "2.0",
        "method": "exit",
        "params": {}
    })
    process.wait()
    print("\nLSP tester finished.")
