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
import tempfile
from .exceptions import NetworkError

class Downloader:
    """Downloads packages from the registry and puts them in cache."""
    
    def __init__(self, registry, cache):
        self.registry = registry
        self.cache = cache
        
    def fetch(self, name: str, version: str) -> str:
        """Returns the path to the cached zip."""
        if self.cache.is_cached(name, version):
            return self.cache.get(name, version)
            
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_zip = os.path.join(tmpdir, f"{name}.zip")
            success = self.registry.download(name, version, temp_zip)
            
            if not success:
                raise NetworkError(f"Failed to download {name}@{version}")
                
            # Store in cache
            return self.cache.store(name, version, temp_zip)
