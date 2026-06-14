"""
Aayu IR Generator (Sprint 25)

Deterministically converts a structurally valid AayuAST into an IRModel.
Removes syntax metadata and unifies entities/shared entities for code generation.
"""

from .ast_nodes import AayuAST
from .ir_nodes import IRModel, IRDomain, IREntity, IRFeature, IRRelationship

class IRGenerator:
    def __init__(self):
        pass

    def generate(self, ast: AayuAST) -> IRModel:
        """
        Converts an AayuAST to an IRModel deterministically.
        Assumes the AST has already passed SemanticAnalyzer validation.
        """
        model = IRModel(system_name=ast.system.name)

        # Map Domains
        for d in ast.domains:
            model.domains.append(IRDomain(name=d.name))

        # Map Entities (Local)
        for e in ast.entities:
            model.entities.append(IREntity(
                name=e.name,
                category=e.type,
                is_shared=False
            ))

        # Map Shared Entities
        for s in ast.shared:
            model.entities.append(IREntity(
                name=s.name,
                category=s.type,
                is_shared=True
            ))

        # Map Features
        for f in ast.features:
            model.features.append(IRFeature(
                name=f.name,
                category=f.type
            ))

        # Map Relationships
        for r in ast.relations:
            model.relationships.append(IRRelationship(
                source=r.source,
                target=r.target,
                cardinality=r.type
            ))

        return model
