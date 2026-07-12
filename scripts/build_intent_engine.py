import os

intent_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine'

# semantic_graph.py
with open(os.path.join(intent_dir, 'semantic_graph.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class SemanticNode:
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos
        self.dependencies = []

    def add_dependency(self, rel_type, target_node):
        self.dependencies.append({"rel": rel_type, "target": target_node})

class SemanticGraph:
    def __init__(self):
        self.nodes = []
        
    def build_from_tagged(self, tagged_tokens):
        # A simple linear parse tree mapping for offline offline intent reasoning
        nodes = [SemanticNode(t, p) for t, p in tagged_tokens]
        # Basic noun-verb linking
        current_verb = None
        for node in nodes:
            if node.pos == "VERB":
                current_verb = node
            elif node.pos == "NOUN" and current_verb:
                current_verb.add_dependency("DOBJ", node)
        
        self.nodes = nodes
        return self
''')

# knowledge_graph.py
with open(os.path.join(intent_dir, 'knowledge_graph.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class KnowledgeNode:
    def __init__(self, name):
        self.entity = name
        self.fields = []
        self.relations = []
        self.events = []
        self.commands = []
        self.policies = []
        self.constraints = []
        self.templates = []
        self.examples = []
        self.security_rules = []
        self.performance_rules = []
        self.deployment_rules = []
        self.cost_rules = []

class KnowledgeGraph:
    def __init__(self):
        self.registry = {}
        # Pre-seed with basic domains
        self._seed_default_domains()
        
    def _seed_default_domains(self):
        # Example Domain: Database
        db_node = KnowledgeNode("database")
        db_node.fields = ["host", "port", "credentials"]
        db_node.security_rules = ["Encrypt at rest", "No public access"]
        db_node.performance_rules = ["Connection pooling enabled", "Indexes on foreign keys"]
        
        # Example Domain: API
        api_node = KnowledgeNode("api")
        api_node.fields = ["routes", "middleware"]
        api_node.security_rules = ["Rate limiting", "Authentication"]
        api_node.performance_rules = ["Response caching"]
        
        self.registry["database"] = db_node
        self.registry["api"] = api_node

    def resolve(self, semantic_graph):
        resolved_nodes = []
        for snode in semantic_graph.nodes:
            if snode.pos == "NOUN":
                name = snode.token.lower()
                if name in self.registry:
                    resolved_nodes.append(self.registry[name])
                else:
                    # Dynamic node generation
                    dyn_node = KnowledgeNode(name)
                    resolved_nodes.append(dyn_node)
        return resolved_nodes
''')

# constraint_resolver.py
with open(os.path.join(intent_dir, 'constraint_resolver.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class ConstraintResolver:
    def resolve(self, constraints_list):
        resolved = {
            "security": "standard",
            "performance": "standard",
            "availability": "99.9",
            "budget": "medium",
            "latency": "medium"
        }
        
        for constraint in constraints_list:
            c = constraint.lower()
            if "fast" in c or "high throughput" in c or "performance" in c:
                resolved["performance"] = "high"
                resolved["latency"] = "low"
            if "secure" in c or "encrypted" in c:
                resolved["security"] = "high"
            if "cheap" in c or "low cost" in c:
                resolved["budget"] = "low"
                
        return resolved
''')

# intent_ir.py
with open(os.path.join(intent_dir, 'intent_ir.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class IntentIR:
    def __init__(self):
        self.goal = ""
        self.domains = []
        self.entities = []
        self.constraints = []
        self.non_functional = {
            "security": "",
            "performance": "",
            "availability": "",
            "budget": "",
            "latency": ""
        }
        self.deployment = {}
        self.architecture = {}
        self.workflows = []
        self.clarifications = []
        self.confidence = 0.0

    def to_dict(self):
        return {
            "goal": self.goal,
            "domains": self.domains,
            "entities": self.entities,
            "constraints": self.constraints,
            "non_functional": self.non_functional,
            "deployment": self.deployment,
            "architecture": self.architecture,
            "workflows": self.workflows,
            "clarifications": self.clarifications,
            "confidence": self.confidence
        }
''')

print("Created Phase 1 Intent Engine Files")
