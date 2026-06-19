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
