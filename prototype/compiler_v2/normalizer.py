import re

class Normalizer:
    def __init__(self):
        # We will canonicalize all these to 'nahi' or mark them as [NEG]
        self.negators = ['nahi', 'nahin', 'nhi', 'nai', 'nah', 'mat', 'na', 'bina', 'without', 'no', 'not']
        
    def normalize(self, text):
        text = text.lower().strip()
        text = re.sub(r'([.,?!])', r' \1 ', text)
        words = text.split()
        
        tokens = []
        for i, word in enumerate(words):
            if word in self.negators:
                tokens.append({"word": word, "tag": "[NEG]", "index": i})
            elif word in [',', '.', '?', '!']:
                tokens.append({"word": word, "tag": "[PUNCT]", "index": i})
            else:
                tokens.append({"word": word, "tag": "[WORD]", "index": i})
                
        return {"raw": text, "tokens": tokens}

if __name__ == "__main__":
    n = Normalizer()
    result = n.normalize("OTP nhi aaya")
    import json
    print(json.dumps(result, indent=2))
