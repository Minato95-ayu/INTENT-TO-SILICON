"""
Aayu Semantic Analyzer (Sprint 23)

Validates the logical consistency of the Abstract Syntax Tree (AST).
Answers "Does this architecture make sense?" rather than "Is the syntax valid?".
"""

from dataclasses import dataclass, field
from typing import List, Set
from .ast_nodes import AayuAST, ASTNode

@dataclass
class SemanticError:
    message: str
    line: int
    column: int
    
    def __str__(self):
        return f"SemanticError: {self.message} at Line {self.line}, Column {self.column}"

@dataclass
class SemanticWarning:
    message: str
    line: int
    column: int
    
    def __str__(self):
        return f"SemanticWarning: {self.message} at Line {self.line}, Column {self.column}"

@dataclass
class SemanticResult:
    valid: bool
    errors: List[SemanticError] = field(default_factory=list)
    warnings: List[SemanticWarning] = field(default_factory=list)


class SemanticAnalyzer:
    def __init__(self):
        pass

    def analyze(self, ast: AayuAST) -> SemanticResult:
        errors: List[SemanticError] = []
        warnings: List[SemanticWarning] = []
        
        # Rule 5: Empty System Check
        if not ast.domains and not ast.entities and not ast.shared and not ast.relations:
            errors.append(SemanticError(
                "System has no architectural content (missing domains, entities, or relations)",
                ast.system.line,
                ast.system.column
            ))
            return SemanticResult(valid=False, errors=errors)

        # Gather all declared domains, entities, and shared
        declared_domains: Set[str] = set()
        declared_entities: Set[str] = set()
        declared_shared: Set[str] = set()
        
        # Rule 3: Duplicate Domain
        for d in ast.domains:
            if d.name in declared_domains:
                errors.append(SemanticError(f"Duplicate domain declaration: '{d.name}'", d.line, d.column))
            declared_domains.add(d.name)
            
        # Rule 2: Duplicate Declaration (Shared)
        for s in ast.shared:
            if s.name in declared_shared:
                errors.append(SemanticError(f"Duplicate shared entity declaration: '{s.name}'", s.line, s.column))
            declared_shared.add(s.name)
            
        # Rule 2 & Rule 4: Duplicate Declaration (Entities) and Shared vs Local Collision
        for e in ast.entities:
            if e.name in declared_entities:
                errors.append(SemanticError(f"Duplicate entity declaration: '{e.name}'", e.line, e.column))
            if e.name in declared_shared:
                errors.append(SemanticError(f"Shared vs Local Collision: '{e.name}' is declared as both shared and local entity", e.line, e.column))
            declared_entities.add(e.name)
            
        all_valid_entities = declared_entities.union(declared_shared)
        
        # Rule 1: Undefined Entity Reference in Relations
        used_entities: Set[str] = set()
        for r in ast.relations:
            if r.source not in all_valid_entities:
                errors.append(SemanticError(f"Undefined entity reference in relation source: '{r.source}'", r.line, r.column))
            else:
                used_entities.add(r.source)
                
            if r.target not in all_valid_entities:
                errors.append(SemanticError(f"Undefined entity reference in relation target: '{r.target}'", r.line, r.column))
            else:
                used_entities.add(r.target)
                
        # Optional Warning: Orphan Entity Detection
        if not errors: # Only check warnings if valid architecture
            for e in ast.entities:
                if e.name not in used_entities and ast.relations: # Only warn if there are some relations
                    warnings.append(SemanticWarning(f"Orphan Entity: '{e.name}' is never used in any relations", e.line, e.column))
                    
            for s in ast.shared:
                if s.name not in used_entities and ast.relations:
                    warnings.append(SemanticWarning(f"Orphan Shared Entity: '{s.name}' is never used in any relations", s.line, s.column))

        return SemanticResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
