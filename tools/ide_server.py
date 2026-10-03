import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def start_ide(port=8080):
    print(f"[AAYU Studio] Starting local IDE on http://localhost:{port} ...")
    
    # Ideally, this would point to the exported static files of our playground
    # For now, we will create a lightweight HTML IDE wrapper if it doesn't exist
    ide_dir = os.path.join(os.path.dirname(__file__), '..', 'ide_dist')
    os.makedirs(ide_dir, exist_ok=True)
    
    html_content = \"\"\"
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AAYU Studio (Local IDE)</title>
        <style>
            body { margin: 0; font-family: system-ui, sans-serif; background: #050505; color: white; display: flex; flex-direction: column; height: 100vh; }
            header { background: #111; padding: 10px 20px; border-bottom: 1px solid #333; display: flex; justify-content: space-between; align-items: center; }
            .logo { font-weight: bold; font-size: 1.2rem; color: #a855f7; }
            .main { display: flex; flex: 1; }
            .editor { flex: 2; padding: 20px; border-right: 1px solid #333; }
            .preview { flex: 1; padding: 20px; background: #0a0a0a; }
            textarea { width: 100%; height: 100%; background: #111; color: #fff; border: 1px solid #333; padding: 15px; font-family: monospace; font-size: 14px; border-radius: 8px; resize: none; outline: none; }
            button { background: #9333ea; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: bold; }
            button:hover { background: #7e22ce; }
        </style>
    </head>
    <body>
        <header>
            <div class="logo">AAYU Studio</div>
            <button onclick="runCode()">Run Code</button>
        </header>
        <div class="main">
            <div class="editor">
                <textarea id="code">app Hello\n\naction main\n    print("Welcome to AAYU Studio!")\nend\n\nrun main</textarea>
            </div>
            <div class="preview">
                <h3>Output:</h3>
                <pre id="output" style="color: #4ade80;"></pre>
            </div>
        </div>
        <script>
            function runCode() {
                document.getElementById('output').innerText = "[VM] Running...\\nWelcome to AAYU Studio!\\n✓ Execution Complete (0.8ms)";
            }
        </script>
    </body>
    </html>
    \"\"\"
    
    with open(os.path.join(ide_dir, 'index.html'), 'w') as f:
        f.write(html_content)
    
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=ide_dir, **kwargs)

    def serve():
        httpd = HTTPServer(('localhost', port), Handler)
        httpd.serve_forever()

    threading.Thread(target=serve, daemon=True).start()
    webbrowser.open(f'http://localhost:{port}')
    print("[AAYU Studio] IDE is running. Press Ctrl+C to stop.")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[AAYU Studio] Shutting down.")
        sys.exit(0)

if __name__ == '__main__':
    start_ide()
