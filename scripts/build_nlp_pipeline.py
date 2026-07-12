import os

intent_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine'

# context_memory.py
with open(os.path.join(intent_dir, 'context_memory.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class ContextMemory:
    def __init__(self):
        self.history = []
        self.active_constraints = set()
        
    def add_interaction(self, prompt, ir):
        self.history.append({"prompt": prompt, "ir": ir})
        for c in ir.constraints:
            self.active_constraints.add(c)
            
    def get_contextual_constraints(self):
        return list(self.active_constraints)
''')

# offline_nlp.py (the orchestrator for Phase 1)
with open(os.path.join(intent_dir, 'offline_nlp.py'), 'w', encoding='utf-8') as f:
    f.write('''\
from .tokenizer import Tokenizer
from .pos_tagger import POSTagger
from .semantic_graph import SemanticGraph
from .knowledge_graph import KnowledgeGraph
from .constraint_resolver import ConstraintResolver
from .intent_ir import IntentIR
from .context_memory import ContextMemory

class OfflineNLPEngine:
    def __init__(self):
        self.tokenizer = Tokenizer()
        self.tagger = POSTagger()
        self.knowledge = KnowledgeGraph()
        self.resolver = ConstraintResolver()
        self.memory = ContextMemory()

    def process(self, prompt: str) -> IntentIR:
        # Pipeline: Tokenizer -> Parser (Tagger) -> Semantic Graph -> Knowledge Graph -> Context Memory -> Constraint Resolver -> Intent IR
        tokens = self.tokenizer.tokenize(prompt)
        tagged = self.tagger.tag(tokens)
        
        sgraph = SemanticGraph().build_from_tagged(tagged)
        knodes = self.knowledge.resolve(sgraph)
        
        raw_constraints = []
        entities = []
        for k in knodes:
            entities.append(k.entity)
            raw_constraints.extend(k.security_rules)
            raw_constraints.extend(k.performance_rules)
            
        # Merge active constraints from memory
        raw_constraints.extend(self.memory.get_contextual_constraints())
        
        resolved_nfrs = self.resolver.resolve(raw_constraints)
        
        ir = IntentIR()
        ir.goal = prompt
        ir.entities = entities
        ir.constraints = raw_constraints
        ir.non_functional = resolved_nfrs
        ir.confidence = 0.95
        
        self.memory.add_interaction(prompt, ir)
        
        return ir
''')

print("Finished Intent Engine Pipeline")
