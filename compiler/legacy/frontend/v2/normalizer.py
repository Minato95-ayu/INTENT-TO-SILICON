"""
=============================================================================
FILE: normalizer.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import json
import os
import re

class Normalizer:
    def __init__(self):
        # We will canonicalize all these to 'nahi' or mark them as [NEG]
        self.negators = ['nahi', 'nahin', 'nhi', 'nai', 'nah', 'mat', 'na', 'bina', 'without', 'no', 'not']
        
        self.root_library = {}
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        try:
            with open(os.path.join(base_dir, 'dictionary', 'root_library.json'), 'r') as f:
                self.root_library = json.load(f)
        except Exception:
            pass
        
    def normalize(self, text):
        text = text.lower().strip()
        
        # Apply morphological replacement
        if self.root_library:
            for canonical_tag, variations in self.root_library.items():
                for variant in sorted(variations, key=len, reverse=True):
                    # Replace longest variants first to prevent partial matching
                    text = text.replace(variant, f"[{canonical_tag}]")
        
        raw_words = text.split()
        
        tokens = []
        for i, word in enumerate(raw_words):
            # Clean punctuation from words unless it's a tag
            clean_word = word
            if not word.startswith('['):
                clean_word = word.strip(',.?!')
                
            if clean_word in self.negators:
                tokens.append({"word": clean_word, "tag": "[NEG]", "index": i})
            elif word.startswith('[') and word.endswith(']'):
                tokens.append({"word": clean_word, "tag": word, "index": i})
            elif word in [',', '.', '?', '!']:
                tokens.append({"word": word, "tag": "[PUNCT]", "index": i})
            else:
                tokens.append({"word": clean_word, "tag": "[WORD]", "index": i})
                
        return {"raw": text, "tokens": tokens}

if __name__ == "__main__":
    n = Normalizer()
    result = n.normalize("verification sms nahi prapt hua")
    import json
    print(json.dumps(result, indent=2))
