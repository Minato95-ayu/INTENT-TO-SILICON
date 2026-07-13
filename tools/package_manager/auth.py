import json
import os

class Auth:
    """Manages ~/.aayu/credentials.json"""
    
    def __init__(self, home_dir: str = None):
        self.home_dir = home_dir or os.path.expanduser("~")
        self.aayu_dir = os.path.join(self.home_dir, ".aayu")
        self.creds_path = os.path.join(self.aayu_dir, "credentials.json")
        os.makedirs(self.aayu_dir, exist_ok=True)
        
    def login(self, token: str):
        with open(self.creds_path, 'w') as f:
            json.dump({"token": token}, f)
            
    def logout(self):
        if os.path.exists(self.creds_path):
            os.remove(self.creds_path)
            
    def is_logged_in(self) -> bool:
        return os.path.exists(self.creds_path)
