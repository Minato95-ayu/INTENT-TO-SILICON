"""
=============================================================================
FILE: intents.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from dataclasses import dataclass

@dataclass
class Intent:
    confidence: float
    source_text: str

@dataclass
class DefineEntityIntent(Intent):
    name: str

@dataclass
class DefineFieldIntent(Intent):
    entity_name: str
    field_name: str

@dataclass
class DefineRelationshipIntent(Intent):
    source: str
    relation: str
    target: str

@dataclass
class DefineTaskIntent(Intent):
    actor: str
    action: str
    target: str
