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

from .registry import Registry

class GithubRegistry(Registry):
    """Stub for Github-based registry resolution."""
    
    def search(self, query: str):
        return [] # GitHub search not implemented natively in CLI
        
    def fetch_manifest(self, package_name: str, version_req: str = None):
        # Implementation would hit api.github.com/repos/user/repo/contents/aayu.json
        raise NotImplementedError("GitHub registry fetch not yet implemented")
        
    def download(self, package_name: str, version: str, dest_path: str):
        raise NotImplementedError("GitHub registry download not yet implemented")
