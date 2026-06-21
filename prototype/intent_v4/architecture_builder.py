import json
from intent_v4.capability_engine import CapabilityEngine
from intent_v4.role_inference import RoleInference
from intent_v4.entity_inference import EntityInference
from intent_v4.relation_inference import RelationInference
from intent_v4.workflow_inference import WorkflowInference

class ArchitectureBuilder:
    def __init__(self):
        self.capability = CapabilityEngine()
        self.role = RoleInference()
        self.entity = EntityInference()
        self.relation = RelationInference()
        self.workflow = WorkflowInference()

    def build(self, intent: str):
        print(f"[*] Parsing Intent: '{intent}'")
        domain = self.capability.parse_intent(intent)
        print(f"[*] Inferred Domain: {domain}")
        
        roles = self.role.infer(domain)
        print(f"[*] Inferred Roles: {len(roles)}")
        
        entities = self.entity.infer(domain)
        print(f"[*] Inferred Entities: {len(entities)}")
        
        relations = self.relation.infer(domain)
        print(f"[*] Inferred Relations: {len(relations)}")
        
        workflow = self.workflow.infer(domain)
        print(f"[*] Inferred Workflow: {workflow.get('name')}")
        
        architecture = {
            "domain": domain,
            "roles": roles,
            "entities": entities,
            "relations": relations,
            "workflow": workflow
        }
        return architecture

if __name__ == "__main__":
    builder = ArchitectureBuilder()
    arch = builder.build("Build a Police Complaint System")
    print("\n" + json.dumps(arch, indent=2))
