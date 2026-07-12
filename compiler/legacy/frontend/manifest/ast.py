"""
=============================================================================
FILE: ast.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

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
