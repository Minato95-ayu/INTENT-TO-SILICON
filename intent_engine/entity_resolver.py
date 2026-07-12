class EntityResolver:
    def resolve(self, entities: list) -> list:
        resolved = []
        for e in entities:
            resolved.append(f"resolved_{e}")
        return resolved
