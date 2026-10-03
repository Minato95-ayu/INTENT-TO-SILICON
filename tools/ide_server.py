import os
import sys
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

def start_ide(port=8080):
    print(f"[AAYU Studio] Starting local IDE on http://localhost:{port} ...")
    
    ide_dir = os.path.join(os.path.dirname(__file__), '..', 'ide_dist')
    os.makedirs(ide_dir, exist_ok=True)
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head><title>AAYU Studio</title></head>
    <body><h1>AAYU Studio Local Server</h1></body>
    </html>
    """
    
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
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    start_ide()
