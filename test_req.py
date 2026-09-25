import asyncio
import time
import urllib.request
import logging
from runtime.renderers.web_renderer import WebRenderer

logging.basicConfig(level=logging.DEBUG)

class DummySessionManager:
    def get_or_create_session(self, id):
        class DummySession:
            session_id = "test"
            current_tree_json = "{}"
        return DummySession()

renderer = WebRenderer(DummySessionManager())
renderer.start()
time.sleep(2)
try:
    r = urllib.request.urlopen('http://127.0.0.1:4000/')
    print(r.getcode())
except Exception as e:
    print("Error:", e)