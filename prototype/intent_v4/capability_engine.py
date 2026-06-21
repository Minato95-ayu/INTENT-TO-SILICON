from intent_v4.knowledge_base import KnowledgeBase

class CapabilityEngine:
    def __init__(self):
        self.kb = KnowledgeBase()

    def parse_intent(self, intent_text: str):
        domain = self.kb.find_domain(intent_text)
        if not domain:
            raise Exception("Unable to infer domain from intent. Please specify a known business domain.")
        return domain
