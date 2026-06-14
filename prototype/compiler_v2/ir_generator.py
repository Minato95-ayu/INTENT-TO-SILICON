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

        # Map Features to capabilities dictionary
        model.capabilities = {
            "auth": False,
            "rbac": False
        }
        
        for f in ast.features:
            model.features.append(IRFeature(
                name=f.name
            ))
            if f.name == "authentication":
                model.capabilities["auth"] = True
            elif f.name == "rbac":
                model.capabilities["rbac"] = True
                # If rbac is specified, it inherently needs auth
                model.capabilities["auth"] = True

        # Inject auth/rbac entities if features are present
        if model.capabilities["auth"]:
            if not any(e.name == "user" for e in model.entities):
                model.entities.append(IREntity(name="user", category="actor", is_shared=True))
            if not any(e.name == "role" for e in model.entities):
                model.entities.append(IREntity(name="role", category="concept", is_shared=True))
                
        if model.capabilities["rbac"]:
            if not any(e.name == "permission" for e in model.entities):
                model.entities.append(IREntity(name="permission", category="concept", is_shared=True))
            
            # Map Many-to-Many relationships for RBAC
            # user <-> role
            if not any(r.source == "user" and r.target == "role" for r in model.relationships):
                model.relationships.append(IRRelationship(source="user", target="role", cardinality="many_to_many"))
            # role <-> permission
            if not any(r.source == "role" and r.target == "permission" for r in model.relationships):
                model.relationships.append(IRRelationship(source="role", target="permission", cardinality="many_to_many"))
        for r in ast.relations:
            model.relationships.append(IRRelationship(
                source=r.source,
                target=r.target,
                cardinality=r.type
            ))

        return model
