import os
import json
from intent_engine.dictionary_loader import DictionaryLoader

class ArchitectureGenerator:
    def __init__(self):
        self.loader = DictionaryLoader()
        self.features = self.loader.get_all_features()
        self.domains = self.loader.get_all_domains()

    def is_affirmative(self, answer: str) -> bool:
        ans = answer.strip().lower()
        return ans in ["yes", "y", "yeah", "yep", "sure", "of course", "true", "1"]

    def generate(self, intent_graph: dict) -> dict:
        if intent_graph.get("status") != "SUCCESS":
            return {"error": "Invalid intent graph"}

        domain_name = intent_graph.get("domain")
        base_entities = list(intent_graph.get("entities", []))
        domain_data = self.domains.get(domain_name, {})
        base_routes = list(domain_data.get("routes", []))
        relations = list(domain_data.get("relations", []))
        
        detected_features = intent_graph.get("detected_features", [])
        user_answers = intent_graph.get("user_answers", {})
        
        final_features = list(detected_features)
        
        # Add features approved by user in cross questions
        for feature_key, answer in user_answers.items():
            if self.is_affirmative(answer):
                if feature_key not in final_features:
                    final_features.append(feature_key)
                    
        # Append entities and routes required by the final features
        for feat in final_features:
            f_data = self.features.get(feat, {})
            f_entities = f_data.get("entities", [])
            for e in f_entities:
                if e not in base_entities:
                    base_entities.append(e)
                    
            f_routes = f_data.get("routes", [])
            for r in f_routes:
                if r not in base_routes:
                    base_routes.append(r)

        schema_relations = []
        # Process Relations (Architecture Generator v2)
        for rel in relations:
            rel_type = rel.get("type")
            if rel_type == "M:N":
                junc = rel.get("junction")
                if junc and junc not in base_entities:
                    base_entities.append(junc)
                schema_relations.append({
                    "from": rel["from"],
                    "to": rel["to"],
                    "type": "M:N",
                    "junction": junc
                })
            elif rel_type == "1:N":
                schema_relations.append({
                    "from": rel["from"],
                    "to": rel["to"],
                    "type": "1:N"
                })
                    
        # Basic Relational Engine: Ensure User/Account entity exists if auth is implied
        has_auth = "auth" in final_features or "/login" in base_routes
        if has_auth:
            if "User" not in base_entities and "Account" not in base_entities:
                base_entities.append("User")
            # Inject Roles & Permissions for v2
            if "Role" not in base_entities:
                base_entities.append("Role")
            if "Permission" not in base_entities:
                base_entities.append("Permission")
                
            # Role mapping relation
            schema_relations.append({
                "from": "User" if "User" in base_entities else "Account",
                "to": "Role",
                "type": "M:N",
                "junction": "UserRole"
            })
            if "UserRole" not in base_entities:
                base_entities.append("UserRole")
            
        architecture = {
            "project_name": f"{domain_name.replace(' ', '')}App",
            "domain": domain_name,
            "auth": has_auth,
            "database": "sqlite",
            "entities": base_entities,
            "relations": schema_relations,
            "routes": base_routes,
            "active_features": final_features
        }
        
        return architecture

if __name__ == "__main__":
    # Mock intent graph for testing Job Portal M:N inference
    mock_intent = {
        "status": "SUCCESS",
        "domain": "Job Portal",
        "entities": ["Candidate", "Job", "Company"],
        "detected_features": [],
        "user_answers": {}
    }
    
    generator = ArchitectureGenerator()
    arch = generator.generate(mock_intent)
    
    print(json.dumps(arch, indent=2))
