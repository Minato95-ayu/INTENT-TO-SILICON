from typing import List, Dict, Any, Union

class ManifestNode:
    def __init__(self, line: int):
        self.line = line

class KeyValueNode(ManifestNode):
    def __init__(self, key: str, value: Any, line: int):
        super().__init__(line)
        self.key = key
        self.value = value

class SectionNode(ManifestNode):
    def __init__(self, name: str, line: int):
        super().__init__(line)
        self.name = name
        self.entries: List[KeyValueNode] = []
        
    def add_entry(self, entry: KeyValueNode):
        self.entries.append(entry)

class ManifestDocument(ManifestNode):
    def __init__(self):
        super().__init__(1)
        self.sections: List[SectionNode] = []
        
    def add_section(self, section: SectionNode):
        self.sections.append(section)
