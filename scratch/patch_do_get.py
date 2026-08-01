import re

with open("runtime/renderers/web_renderer.py", "r", encoding="utf-8") as f:
    content = f.read()

new_do_get = """
    def do_GET(self):
        # API Stream
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
            
        # Serve Static Assets from .aayu/build/
        import os
        import mimetypes
        
        req_path = self.path
        if req_path == "/":
            req_path = "/index.html"
            
        build_dir = os.path.join(_global_project_dir, ".aayu", "build")
        file_path = os.path.abspath(os.path.join(build_dir, req_path.lstrip("/")))
        
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
"""

# We need to replace the current do_GET inside WebRendererHandler.
# The original do_GET starts around line 170 and ends at 480.
# We will use regex to find and replace it.

pattern = re.compile(r"    def do_GET\(self\):.*?    def do_POST\(self\):", re.DOTALL)
new_content = pattern.sub(new_do_get + "\n    def do_POST(self):", content)

with open("runtime/renderers/web_renderer.py", "w", encoding="utf-8") as f:
    f.write(new_content)
