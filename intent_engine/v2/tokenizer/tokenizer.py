"""
=============================================================================
FILE: tokenizer.py
PURPOSE: Tokenizer for Intent Engine v2
=============================================================================
"""

import re
from typing import List

class Tokenizer:
    def __init__(self):
        pass
        
    def tokenize(self, prompt: str) -> List[str]:
        # Split on " and " to handle multi-intent prompts
        intents = re.split(r'\s+and\s+', prompt, flags=re.IGNORECASE)
        
        tokens = []
        for intent in intents:
            # simple word tokenization for heuristics
            words = re.findall(r'\b\w+\b', intent.lower())
            tokens.append(words)
            
        return tokens
