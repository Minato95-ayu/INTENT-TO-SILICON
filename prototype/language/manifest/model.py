from enum import Enum
from typing import List, Dict, Optional, Any
from .version import Version

class DependencySource(Enum):
    LOCAL = "local"
    REGISTRY = "registry"
    GIT = "git"
    WORKSPACE = "workspace"

class Dependency:
    def __init__(self, name: str, version: Optional[Version], source: DependencySource, optional: bool = False, resolved_path: Optional[str] = None):
        self.name = name
        self.version = version
        self.source = source
        self.optional = optional
        self.resolved_path = resolved_path

class PackageInfo:
    def __init__(self, name: str, version: Version, edition: str = "2026"):
        self.name = name
        self.version = version
        self.edition = edition

class BuildInfo:
    def __init__(self, entry: str):
        self.entry = entry

class PackageManifest:
    def __init__(self):
        self.package: Optional[PackageInfo] = None
        self.authors: List[str] = []
        self.dependencies: Dict[str, Dependency] = {}
        self.build: Optional[BuildInfo] = None
        self.metadata: Dict[str, Any] = {} # Reserved for future extensions
