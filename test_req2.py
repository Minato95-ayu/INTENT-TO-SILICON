import asyncio
import time
import subprocess
from runtime.renderers.web_renderer import WebRenderer
class DummySessionManager:
    def get_or_create_session(self, id):
        class DummySession:
            session_id = "test"
            current_tree_json = "{}"
        return DummySession()

renderer = WebRenderer(DummySessionManager())
renderer.start()
time.sleep(2)
subprocess.run(['curl.exe', '-v', 'http://127.0.0.1:4000/'])