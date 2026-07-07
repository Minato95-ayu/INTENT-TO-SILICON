"""
=============================================================================
FILE: validator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import Any
from .ast import ManifestDocument, SectionNode, KeyValueNode
from .model import PackageManifest, PackageInfo, BuildInfo, Dependency, DependencySource
from .version import Version
from compiler.frontend.compiler_context import Diagnostics

class ManifestValidator:
    def __init__(self, diagnostics: Diagnostics, filepath: str):
        self.diagnostics = diagnostics
        self.filepath = filepath

    def validate(self, doc: ManifestDocument) -> PackageManifest:
        manifest = PackageManifest()
        seen_sections = set()
        
        for section in doc.sections:
            if section.name in seen_sections:
                self.diagnostics.error(f"Duplicate section '[{section.name}]'", self.filepath, section.line)
                continue
            seen_sections.add(section.name)
            
            if section.name == "package":
                manifest.package = self._parse_package(section)
            elif section.name == "authors":
                manifest.authors = self._parse_authors(section)
            elif section.name == "build":
                manifest.build = self._parse_build(section)
            elif section.name == "dependencies":
                manifest.dependencies = self._parse_dependencies(section)
            else:
                self.diagnostics.warning(f"Unknown section '[{section.name}]'", self.filepath, section.line)
                # Store in metadata
                manifest.metadata[section.name] = {entry.key: entry.value for entry in section.entries}
                
        if not manifest.package:
            self.diagnostics.error("Missing required section '[package]'", self.filepath)
        if not manifest.build:
            self.diagnostics.error("Missing required section '[build]'", self.filepath)
            
        return manifest

    def _parse_package(self, section: SectionNode) -> PackageInfo:
        seen_keys = set()
        name = None
        version = None
        edition = "2026"
        
        for entry in section.entries:
            if entry.key in seen_keys:
                self.diagnostics.error(f"Duplicate field '{entry.key}' in [package]", self.filepath, entry.line)
                continue
            seen_keys.add(entry.key)
            
            if entry.key == "name":
                name = entry.value
            elif entry.key == "version":
                try:
                    version = Version.parse(entry.value)
                except ValueError as e:
                    self.diagnostics.error(str(e), self.filepath, entry.line)
            elif entry.key == "edition":
                edition = entry.value
            else:
                self.diagnostics.warning(f"Unknown field '{entry.key}' in [package]", self.filepath, entry.line)
                
        if not name:
            self.diagnostics.error("Missing required field 'name' in [package]", self.filepath, section.line)
        if not version:
            self.diagnostics.error("Missing required field 'version' in [package]", self.filepath, section.line)
            
        return PackageInfo(name or "", version or Version(0,0,0), edition)

    def _parse_authors(self, section: SectionNode) -> list:
        authors = []
        for entry in section.entries:
            if entry.key == "names":
                if isinstance(entry.value, list):
                    authors.extend(entry.value)
                else:
                    self.diagnostics.error("Field 'names' must be an array", self.filepath, entry.line)
            else:
                self.diagnostics.warning(f"Unknown field '{entry.key}' in [authors]", self.filepath, entry.line)
        return authors

    def _parse_build(self, section: SectionNode) -> BuildInfo:
        entry_path = None
        for entry in section.entries:
            if entry.key == "entry":
                entry_path = entry.value
            else:
                self.diagnostics.warning(f"Unknown field '{entry.key}' in [build]", self.filepath, entry.line)
                
        if not entry_path:
            self.diagnostics.error("Missing required field 'entry' in [build]", self.filepath, section.line)
            
        return BuildInfo(entry_path or "")

    def _parse_dependencies(self, section: SectionNode) -> dict:
        deps = {}
        for entry in section.entries:
            if entry.key in deps:
                self.diagnostics.error(f"Duplicate dependency '{entry.key}'", self.filepath, entry.line)
                continue
                
            try:
                version = Version.parse(entry.value)
                deps[entry.key] = Dependency(entry.key, version, DependencySource.REGISTRY)
            except ValueError as e:
                self.diagnostics.error(f"Invalid version for dependency '{entry.key}': {e}", self.filepath, entry.line)
                
        return deps
