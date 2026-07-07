import re

class Tokenizer:
    def tokenize(self, text: str) -> list:
        # A robust regex based tokenizer that handles punctuation, quotes, and AAYU syntax natively
        pattern = r"\w+|[^\w\s]"
        return re.findall(pattern, text)
