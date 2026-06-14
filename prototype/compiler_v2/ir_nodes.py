"""
Aayu IR Nodes (Sprint 25)

Defines the Deterministic Intermediate Representation (IR) structures.
Unlike the AST, IR nodes discard syntax metadata (line, column, tokens)
and focus purely on normalized semantic meaning for code generators.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class IRDomain:
    name: str

@dataclass
class IREntity:
    name: str
    category: Optional[str] = None  # e.g., 'actor', 'resource', 'transaction'
    is_shared: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class IRFeature:
    name: str
    category: Optional[str] = None

@dataclass
class IRRelationship:
    source: str
    target: str
    cardinality: Optional[str] = None  # e.g., 'one_to_one', 'one_to_many', 'many_to_many'

@dataclass
class IRModel:
    system_name: str
    domains: List[IRDomain] = field(default_factory=list)
    entities: List[IREntity] = field(default_factory=list)
    features: List[IRFeature] = field(default_factory=list)
    relationships: List[IRRelationship] = field(default_factory=list)
