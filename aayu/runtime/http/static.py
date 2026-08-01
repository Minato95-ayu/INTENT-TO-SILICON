import os
import mimetypes

class StaticEngine:
    def __init__(self, static_dir):
        self.static_dir = static_dir

    def handle(self, ctx):
        # Prevent directory traversal attacks
        safe_path = os.path.normpath(ctx.request.path).lstrip('/')
        full_path = os.path.join(self.static_dir, safe_path)
        
        if not full_path.startswith(self.static_dir):
            ctx.response.status(403).text("Forbidden")
            return True
            
        if os.path.exists(full_path) and os.path.isfile(full_path):
            ctx.response.file(full_path)
            return True
            
        return False # Not handled by static engine
