"""
=============================================================================
FILE: manager.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from enum import Enum
from typing import Dict, Any
from ..values.base import RuntimeValue

class ModuleState(Enum):
    INITIALIZED = "initialized"
    LOADING = "loading"
    LOADED = "loaded"
    FAILED = "failed"

class Module:
    def __init__(self, name: str):
        self.name = name
        self.symbols: Dict[str, RuntimeValue] = {}
        self.exports: Dict[str, RuntimeValue] = {}
        self.imports: list = []
        self.state = ModuleState.INITIALIZED

class ModuleManager:
    def __init__(self, registry: 'ModuleRegistry'):
        self.registry = registry
        self.active_modules: Dict[str, Module] = {}

    def load_module(self, name: str) -> Module:
        if name in self.active_modules:
            return self.active_modules[name]
        
        module = self.registry.get_module(name)
        if not module:
            # If not in global registry, create a new one
            module = Module(name)
            self.registry.register(module)
            
        self.active_modules[name] = module
        return module

class ModuleRegistry:
    """
    Globally available registry for modules.
    """
    def __init__(self):
        self.modules: Dict[str, Module] = {}
        
    def register(self, module: Module):
        self.modules[module.name] = module
        
    def get_module(self, name: str) -> Module:
        return self.modules.get(name)
