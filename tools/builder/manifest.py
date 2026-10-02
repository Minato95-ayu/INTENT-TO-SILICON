import json
import os

class Manifest:
    """Manages project build configuration and manifest."""
    def __init__(self):
        self.config = self._load()
        
    def _load(self):
        if os.path.exists("aayu.json"):
            with open("aayu.json", "r") as f:
                return json.load(f)
        return {"name": "aayu_app", "version": "1.0.0"}
