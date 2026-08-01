import os

with open("runtime/renderers/web_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

# We'll split the content into CSS, JS, and HTML, and save them.
# I'll just write a quick script to find the parts and replace do_GET.

new_content = content.replace('''class WebRendererHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            

            html = \'''
            <!DOCTYPE html>
            <html>
            <head>
                <title>AAYU DOM Renderer</title>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                <style>
                    body { margin: 0; padding: 0; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; background-color: #111b21; color: #e9edef; overflow: hidden; }
                    .widget-container { box-sizing: border-box; display: flex; }
                    .widget-row { display: flex; flex-direction: row; box-sizing: border-box; }
                    .widget-column { display: flex; flex-direction: column; box-sizing: border-box; }
                    .widget-button { cursor: pointer; border: none; outline: none; box-sizing: border-box; transition: background-color 0.2s; display: flex; align-items: center; justify-content: center;}
                    .widget-input { border: 1px solid #ccc; outline: none; box-sizing: border-box; padding: 0 15px; font-family: inherit; }
                    .widget-icon { display: flex; align-items: center; justify-content: center; }
                    .widget-page, .widget-scaffold { width: 100vw; height: 100vh; overflow: hidden; box-sizing: border-box; display: flex; flex-direction: column; }
                    .widget-text { font-family: inherit; }
                    .widget-avatar { object-fit: cover; overflow: hidden; background-color: #ccc; }
                    .widget-chatbubble { max-width: 85%; font-size: 14.2px; }
                    .chat-time { font-size: 11px; color: rgba(255,255,255,0.6); align-self: flex-end; margin-top: 4px; }
                    
                    ::-webkit-scrollbar { width: 6px; }
                    ::-webkit-scrollbar-track { background: transparent; }
                    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }
                    
                    #root { width: 100vw; height: 100vh; }
                </style>
                <style id="dynamic-styles"></style>
            </head>
            <body>
                <div id="root"></div>
                <script>''', '''import mimetypes
import os

_global_project_dir = "."

class WebRendererHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve API stream
        if self.path == "/api/stream":
            self.send_response(200)
            self.send_header('Content-type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Connection', 'keep-alive')
            self.end_headers()
            
            import queue
            q = queue.Queue()
            _clients.append(q)
            
            try:
                initial = f"data: {_current_tree_json}\\n\\n"
                self.wfile.write(initial.encode('utf-8'))
                self.wfile.flush()
                
                while True:
                    data = q.get()
                    msg = f"data: {data}\\n\\n"
                    self.wfile.write(msg.encode('utf-8'))
                    self.wfile.flush()
            except Exception:
                pass
            finally:
                if q in _clients:
                    _clients.remove(q)
            return

        # Serve static files from .aayu/build/
        req_path = self.path
        if req_path == "/":
            req_path = "/index.html"
            
        build_dir = os.path.join(_global_project_dir, ".aayu", "build")
        file_path = os.path.abspath(os.path.join(build_dir, req_path.lstrip("/")))
        
        # Security check: ensure path is within build_dir
        if not file_path.startswith(os.path.abspath(build_dir)):
            self.send_response(403)
            self.end_headers()
            return
            
        if os.path.exists(file_path) and os.path.isfile(file_path):
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type:
                self.send_header("Content-type", mime_type)
            self.end_headers()
            
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_response(404)
            self.end_headers()

    # DUMMY_TO_REPLACE_THE_REST''')

# Wait, `DUMMY_TO_REPLACE_THE_REST` is because we need to strip out the rest of the JS and HTML.
import re

new_content = re.sub(
    r"html = '''\s*<!DOCTYPE html>.*?self\.wfile\.write\(html\.encode\('utf-8'\)\)",
    r"",
    content,
    flags=re.DOTALL
)

with open("scratch/patched_web_renderer.py", "w", encoding="utf-8") as f:
    f.write(new_content)

