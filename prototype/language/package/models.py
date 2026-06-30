from typing import Any, Optional
from manifest.model import PackageManifest, Version

class InstalledPackage:
    def __init__(self, name: str, version: Version, location: str, manifest: PackageManifest, hash: Optional[str] = None):
        self.name = name
        self.version = version
        self.location = location
        self.manifest = manifest
        self.hash = hash
