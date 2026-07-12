"""
=============================================================================
FILE: compiler.py
PURPOSE: Bytecode Compiler - Converts AST to executable bytecode
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles bytecode compiler - converts ast to executable bytecode.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from compiler.frontend.v2.normalizer import Normalizer
from compiler.frontend.v2.pain_point_extractor import PainPointExtractor
from compiler.frontend.v2.aayu_ir import AayuIRBuilder
from compiler.frontend.v2.aayu_codegen import PythonGenerator
import json

class CompilerV2:
    def __init__(self):
        self.normalizer = Normalizer()
        self.extractor = PainPointExtractor()
        self.aayu_builder = AayuIRBuilder()
        self.codegen = PythonGenerator()
        
    def process(self, input_text):
        normalized = self.normalizer.normalize(input_text)
        intent_ir = self.extractor.extract(normalized)
        
        aayu_ir = self.aayu_builder.build(intent_ir)
        code = self.codegen.generate(aayu_ir)
        
        return {
            "raw": input_text,
            "normalized_tokens": normalized.get("tokens", []),
            "intent_ir": intent_ir,
            "aayu_ir": aayu_ir,
            "code": code
        }

if __name__ == "__main__":
    c = CompilerV2()
    print("=== Intent Compiler V2 Alpha ===")
    test_phrase = "paise kat gaye par order nahi bana"
    print(f"Input: {test_phrase}")
    res = c.process(test_phrase)
    print("\n--- Intent IR ---")
    print(json.dumps(res['intent_ir'], indent=2))
    print("\n--- Aayu IR ---")
    print(json.dumps(res['aayu_ir'], indent=2))
    print("\n--- Python Code ---")
    print(res['code'])
