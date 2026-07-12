import os
import re

intent_dir = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\intent_engine'

with open(os.path.join(intent_dir, 'tokenizer.py'), 'w', encoding='utf-8') as f:
    f.write('''\
import re

class Tokenizer:
    def tokenize(self, text: str) -> list:
        # A robust regex based tokenizer that handles punctuation, quotes, and AAYU syntax natively
        pattern = r"\\w+|[^\\w\\s]"
        return re.findall(pattern, text)
''')

with open(os.path.join(intent_dir, 'pos_tagger.py'), 'w', encoding='utf-8') as f:
    f.write('''\
class POSTagger:
    def __init__(self):
        # A small offline lexicon for AAYU specific semantics
        self.lexicon = {
            "create": "VERB",
            "build": "VERB",
            "make": "VERB",
            "database": "NOUN",
            "api": "NOUN",
            "fast": "ADJ",
            "secure": "ADJ",
            "a": "DET",
            "the": "DET",
            "with": "PREP"
        }

    def tag(self, tokens: list) -> list:
        tagged = []
        for token in tokens:
            lower = token.lower()
            if lower in self.lexicon:
                tagged.append((token, self.lexicon[lower]))
            elif lower.endswith('ly'):
                tagged.append((token, "ADV"))
            elif lower.endswith('ing') or lower.endswith('ed'):
                tagged.append((token, "VERB"))
            elif lower.isalnum():
                tagged.append((token, "NOUN"))
            else:
                tagged.append((token, "PUNCT"))
        return tagged
''')

print("Fixed intent engine NLP")
