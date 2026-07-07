import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine\__init__.py'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write('''
from .tokenizer import Tokenizer
from .pos_tagger import POSTagger
from .context_memory import ContextMemory
from .intent_history import IntentHistory
from .domain_detection import DomainDetection
from .semantic_parser import SemanticParser
from .entity_resolver import EntityResolver
''')

print("Updated intent_engine init")
