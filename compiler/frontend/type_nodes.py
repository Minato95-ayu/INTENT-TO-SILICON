"""
=============================================================================
FILE: type_nodes.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from typing import List, Optional
from compiler.frontend.ast_nodes import Node

class TypeNode(Node):
    """Base class for all type annotations."""
    pass

class PrimitiveTypeNode(TypeNode):
    def __init__(self, name: str):
        self.name = name

    def to_dict(self):
        return {"type": "PrimitiveType", "name": self.name}

class NamedTypeNode(TypeNode):
    def __init__(self, name: str):
        self.name = name
        
    def to_dict(self):
        return {"type": "NamedType", "name": self.name}

class GenericTypeNode(TypeNode):
    def __init__(self, base_type: TypeNode, type_args: List[TypeNode]):
        self.base_type = base_type
        self.type_args = type_args
        
    def to_dict(self):
        return {
            "type": "GenericType",
            "base": self.base_type.to_dict(),
            "args": [a.to_dict() for a in self.type_args]
        }

class FunctionTypeNode(TypeNode):
    def __init__(self, param_types: List[TypeNode], return_type: Optional[TypeNode]):
        self.param_types = param_types
        self.return_type = return_type
        
    def to_dict(self):
        return {
            "type": "FunctionType",
            "params": [p.to_dict() for p in self.param_types],
            "return": self.return_type.to_dict() if self.return_type else None
        }

class UnionTypeNode(TypeNode):
    def __init__(self, types: List[TypeNode]):
        self.types = types
        
    def to_dict(self):
        return {
            "type": "UnionType",
            "types": [t.to_dict() for t in self.types]
        }

class OptionalTypeNode(TypeNode):
    def __init__(self, inner_type: TypeNode):
        self.inner_type = inner_type
        
    def to_dict(self):
        return {
            "type": "OptionalType",
            "inner": self.inner_type.to_dict()
        }
