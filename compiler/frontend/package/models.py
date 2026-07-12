"""
=============================================================================
FILE: models.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import Any, Optional
from manifest.model import PackageManifest, Version

class InstalledPackage:
    def __init__(self, name: str, version: Version, location: str, manifest: PackageManifest, hash: Optional[str] = None):
        self.name = name
        self.version = version
        self.location = location
        self.manifest = manifest
        self.hash = hash
