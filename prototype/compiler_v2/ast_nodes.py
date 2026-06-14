"""
Aayu AST Nodes (Sprint 22)

Defines the Abstract Syntax Tree data structures for Aayu Grammar v0.1.
All nodes preserve source code line and column metadata for future semantic errors.
"""

from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ASTNode:
    """Base class for all AST nodes."""
    line: int
    column: int

@dataclass
class SystemNode(ASTNode):
    name: str

@dataclass
class DomainNode(ASTNode):
    name: str

@dataclass
class SharedNode(ASTNode):
    name: str

@dataclass
class EntityNode(ASTNode):
    name: str

@dataclass
class FeatureNode(ASTNode):
    name: str

@dataclass
class RelationNode(ASTNode):
    source: str
    target: str

@dataclass
class AayuAST:
    """Root node of the Abstract Syntax Tree."""
    system: SystemNode
    domains: List[DomainNode] = field(default_factory=list)
    shared: List[SharedNode] = field(default_factory=list)
    entities: List[EntityNode] = field(default_factory=list)
    features: List[FeatureNode] = field(default_factory=list)
    relations: List[RelationNode] = field(default_factory=list)
