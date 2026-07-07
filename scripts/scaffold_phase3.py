import os

intent_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine"

def write_file(path, content):
    full_path = os.path.join(intent_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

write_file("tokenizer.py", """\
class Tokenizer:
    def tokenize(self, text: str) -> list:
        # Simple whitespace tokenizer for offline NLP
        return text.split()
""")

write_file("pos_tagger.py", """\
class POSTagger:
    def tag(self, tokens: list) -> list:
        # Dummy POS tagger
        return [(token, "NOUN") for token in tokens]
""")

write_file("context_memory.py", """\
class ContextMemory:
    def __init__(self):
        self.memory = {}
    def set(self, key, value):
        self.memory[key] = value
    def get(self, key):
        return self.memory.get(key)
""")

write_file("intent_history.py", """\
class IntentHistory:
    def __init__(self):
        self.history = []
    def add(self, intent):
        self.history.append(intent)
    def get_last(self):
        return self.history[-1] if self.history else None
""")

write_file("domain_detection.py", """\
class DomainDetection:
    def detect(self, text: str) -> str:
        text = text.lower()
        if "user" in text or "login" in text:
            return "auth"
        if "pay" in text or "cart" in text:
            return "ecommerce"
        return "general"
""")

write_file("semantic_parser.py", """\
class SemanticParser:
    def parse(self, text: str) -> dict:
        return {"action": "create", "subject": "unknown"}
""")

write_file("entity_resolver.py", """\
class EntityResolver:
    def resolve(self, entities: list) -> list:
        resolved = []
        for e in entities:
            resolved.append(f"resolved_{e}")
        return resolved
""")

print("Phase 3 scaffolding complete")
