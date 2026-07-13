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
