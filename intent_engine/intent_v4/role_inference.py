"""
=============================================================================
FILE: role_inference.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from intent_v4.knowledge_base import KnowledgeBase

class RoleInference:
    def __init__(self):
        self.domains = KnowledgeBase.get_domains()

    def infer(self, domain: str):
        data = self.domains.get(domain, {})
        return data.get("roles", [])
