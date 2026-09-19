# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import os
import json
import shutil
import urllib.request
import urllib.parse
from .registry import Registry

class OfficialRegistry(Registry):
    def __init__(self, cache_dir: str):
        # AAYU Enterprise Self-Hosting capability
        self.registry_url = os.environ.get("AAYU_REGISTRY_URL", "http://localhost:5000")
        self.cache_dir = cache_dir
        
        # We keep the local mock directory just for caching
        self.registry_dir = os.path.join(cache_dir, "registry_mock")
        os.makedirs(self.registry_dir, exist_ok=True)
        
    def _get_pkg_dir(self, name: str):
        return os.path.join(self.registry_dir, name)
        
    def search(self, query: str):
        try:
            req = urllib.request.Request(f"{self.registry_url}/search?q={urllib.parse.quote(query)}")
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"[Registry] Warning: Could not connect to {self.registry_url}")
            return []
        
    def fetch_manifest(self, package_name: str, version_req: str = None):
        try:
            req = urllib.request.Request(f"{self.registry_url}/manifest/{urllib.parse.quote(package_name)}")
            with urllib.request.urlopen(req, timeout=5) as response:
                return json.loads(response.read().decode())
        except Exception:
            return None
            
    def download(self, package_name: str, version: str, dest_path: str):
        try:
            req = urllib.request.Request(f"{self.registry_url}/download/{urllib.parse.quote(package_name)}/{urllib.parse.quote(version)}")
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(dest_path, 'wb') as f:
                    f.write(response.read())
            return True
        except Exception:
            return False
        
    def publish(self, manifest_data: dict, zip_path: str):
        import uuid
        boundary = uuid.uuid4().hex
        
        headers = {'Content-type': f'multipart/form-data; boundary={boundary}'}
        
        body = []
        body.append(f'--{boundary}'.encode())
        body.append(b'Content-Disposition: form-data; name="manifest"')
        body.append(b'')
        body.append(json.dumps(manifest_data).encode())
        
        with open(zip_path, 'rb') as f:
            zip_content = f.read()
            
        body.append(f'--{boundary}'.encode())
        body.append(f'Content-Disposition: form-data; name="file"; filename="{manifest_data["version"]}.zip"'.encode())
        body.append(b'Content-Type: application/zip')
        body.append(b'')
        body.append(zip_content)
        
        body.append(f'--{boundary}--'.encode())
        body.append(b'')
        
        data = b'\r\n'.join(body)
        
        try:
            req = urllib.request.Request(f"{self.registry_url}/publish", data=data, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                res = json.loads(response.read().decode())
                return res.get("status") == "success"
        except Exception as e:
            print(f"[Registry] Publish failed: {e}")
            return False
