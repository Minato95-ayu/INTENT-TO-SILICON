from intent_v4.knowledge_base import KnowledgeBase

class RelationInference:
    def __init__(self):
        self.domains = KnowledgeBase.get_domains()

    def infer(self, domain: str):
        data = self.domains.get(domain, {})
        return data.get("relations", [])
