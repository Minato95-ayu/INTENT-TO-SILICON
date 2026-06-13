from normalizer import Normalizer
from pain_point_extractor import PainPointExtractor
import json

class CompilerV2:
    def __init__(self):
        self.normalizer = Normalizer()
        self.extractor = PainPointExtractor()
        
    def process(self, input_text):
        normalized = self.normalizer.normalize(input_text)
        ir = self.extractor.extract(normalized)
        return ir

if __name__ == "__main__":
    c = CompilerV2()
    print("=== Intent Compiler V2 ===")
    test_phrase = "mujhe payment ka koi dar nahi hai"
    print(f"Input: {test_phrase}")
    print("Tokens:", c.normalizer.normalize(test_phrase)['tokens'])
    print("IR Output:", json.dumps(c.process(test_phrase), indent=2))
