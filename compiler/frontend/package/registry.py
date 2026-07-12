"""
=============================================================================
FILE: registry.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import shutil
from typing import Optional
from manifest.model import PackageManifest, Version
from manifest.lexer import ManifestLexer
from manifest.parser import ManifestParser
from manifest.validator import ManifestValidator
from compiler.frontend.compiler_context import Diagnostics

class RegistryClient:
    def resolve(self, name: str, version: Optional[Version]) -> Optional[PackageManifest]:
        raise NotImplementedError()
        
    def download(self, name: str, version: Optional[Version], target_dir: str) -> bool:
        raise NotImplementedError()
        
    def publish(self):
        raise NotImplementedError()
        
    def search(self):
        raise NotImplementedError()
        
    def metadata(self):
        raise NotImplementedError()

class LocalRegistry(RegistryClient):
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        
    def resolve(self, name: str, version: Optional[Version]) -> Optional[PackageManifest]:
        pkg_dir = os.path.join(self.registry_path, name)
        manifest_path = os.path.join(pkg_dir, "Aayu.toml")
        
        if not os.path.exists(manifest_path):
            return None
            
        diagnostics = Diagnostics()
        try:
            with open(manifest_path, 'r', encoding='utf-8') as f:
                source = f.read()
            lexer = ManifestLexer(source)
            tokens = lexer.tokenize()
            parser = ManifestParser(tokens)
            ast_doc = parser.parse()
            validator = ManifestValidator(diagnostics, manifest_path)
            manifest = validator.validate(ast_doc)
            
            if diagnostics.has_errors():
                return None
                
            # Naive version check for LocalRegistry
            if version and str(manifest.package.version) != str(version):
                return None
                
            return manifest
        except Exception:
            return None

    def download(self, name: str, version: Optional[Version], target_dir: str) -> bool:
        pkg_dir = os.path.join(self.registry_path, name)
        if not os.path.exists(pkg_dir):
            return False
            
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
            
        shutil.copytree(pkg_dir, target_dir)
        return True
