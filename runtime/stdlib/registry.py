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

from typing import Dict, Callable, Any
from ..values.base import RuntimeValue
from ..values.null import NullValue

class StdLibRegistry:
    def __init__(self):
        self.functions: Dict[str, Callable] = {}
        
    def register(self, name: str, func: Callable):
        self.functions[name] = func
        
    def lookup(self, name: str) -> bool:
        return name in self.functions
        
    def _create_method_dispatcher(self, method_name: str):
        def dispatcher(args, vm):
            if not args:
                raise Exception(f"Method call {method_name} missing target object")
            obj = args[0]
            if isinstance(obj, list):
                type_name = "list"
            elif isinstance(obj, dict):
                type_name = "map"
            elif isinstance(obj, str):
                type_name = "string"
            else:
                type_name = obj.type_name() if hasattr(obj, 'type_name') else type(obj).__name__
            specific_name = f"{type_name}_{method_name}"
            if specific_name in self.functions:
                return self.functions[specific_name](args, vm)
            
            generic_name = f"collection_{method_name}"
            if generic_name in self.functions:
                return self.functions[generic_name](args, vm)
                
            from ..values.collection import CollectionValue
            if isinstance(obj, CollectionValue):
                func = getattr(obj, method_name, None)
                if func:
                    return func(*args[1:])
            raise Exception(f"Method {method_name} not found on {type_name}")
        return dispatcher

    def register_method(self, method_name: str):
        name = f"__method_{method_name}"
        if name not in self.functions:
            self.functions[name] = self._create_method_dispatcher(method_name)

    def call(self, name: str, args: list, vm) -> RuntimeValue:
        if name not in self.functions:
            raise Exception(f"Unknown stdlib function: {name}")
        return self.functions[name](args, vm)
