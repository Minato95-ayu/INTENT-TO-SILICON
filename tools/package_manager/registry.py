from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class Registry(ABC):
    """Abstract Base Class for all package registries."""
    
    @abstractmethod
    def search(self, query: str) -> List[dict]:
        pass
        
    @abstractmethod
    def fetch_manifest(self, package_name: str, version_req: str = None) -> Optional[dict]:
        """Fetch the manifest containing available versions and checksums."""
        pass
        
    @abstractmethod
    def download(self, package_name: str, version: str, dest_path: str) -> bool:
        """Download a specific package version to a destination."""
        pass
