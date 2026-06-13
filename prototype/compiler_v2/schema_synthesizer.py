import json
import os

class CompilerError(Exception):
    pass

class SchemaSynthesizer:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.ontology = self._load_ontology()

    def _load_ontology(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ontology_path = os.path.join(base_dir, 'dictionary', 'domain_ontology.json')
        try:
            with open(ontology_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading domain ontology: {e}")
            return {"entities": {}, "domains": {}}

    def synthesize(self, data_entities):
        """
        Takes a list of concepts (e.g. ['patient', 'doctor', 'appointment'])
        and synthesizes a full relational schema using the Domain Ontology.
        """
        resolved_schema = {}
        for entity in data_entities:
            entity_name = entity.lower().replace(' ', '_')
            
            # 1. Lookup entity in Ontology
            if entity_name not in self.ontology.get('entities', {}):
                raise CompilerError(f"""
Aayu Compiler Error

Unknown Entity: '{entity_name}'

Suggestions:
1. Define ontology entry in dictionary/domain_ontology.json
2. Add custom entity specification
3. Answer clarification questions
""")
                
            ontology_def = self.ontology['entities'][entity_name]
            
            # 2. Extract fields
            fields = ontology_def.get('fields', []).copy()
            
            # Always add ID and created_at
            fields.insert(0, {"name": "id", "type": "string", "primary_key": True})
            fields.append({"name": "created_at", "type": "datetime", "default": "CURRENT_TIMESTAMP"})
            
            # 3. Extract relations and convert to Foreign Keys
            relations = ontology_def.get('relations', [])
            for rel in relations:
                fields.append({
                    "name": f"{rel}_id",
                    "type": "string",
                    "foreign_key": f"{rel}.id"
                })
            
            # 4. Compile into resolved schema format
            resolved_schema[entity_name] = {
                "fields": fields,
                "relations": relations
            }
            
        return resolved_schema
