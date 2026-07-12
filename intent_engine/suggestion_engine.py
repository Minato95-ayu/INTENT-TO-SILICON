"""
=============================================================================
FILE: suggestion_engine.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

class SuggestionEngine:
    def __init__(self):
        # In a production environment, this could be backed by an LLM, 
        # a Knowledge Graph, or rich Domain Models.
        self.knowledge_base = {
            "Student": ["name", "age", "phone", "email", "roll_number"],
            "Library": ["name", "owner", "address", "capacity", "books"],
            "Book": ["title", "author", "isbn", "price"],
        }
        
    def get_common_fields(self, entity_name: str) -> list:
        """Dynamically fetch commonly associated fields for a given entity."""
        # For the prototype, we fall back to generic fields if entity is unknown.
        return self.knowledge_base.get(entity_name, ["id", "name", "description"])
