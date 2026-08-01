from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder

# Ek simple AAYU code (like toggling a state, similar to toggling an LED)
aayu_code = """
state led_status = 0

action toggle_led()
  if led_status == 0
    led_status = 1
    print("LED is ON")
  else
    led_status = 0
    print("LED is OFF")
  end
end
"""

# Compilation Pipeline (Bypassing Traditional Compilers)
tokens = Lexer(aayu_code).tokenize()
ast = Parser(tokens).parse()
semantic_ast = SemanticAnalyzer().analyze(ast)

pipe = IRPipeline()
hir = pipe.to_hir(semantic_ast)
mir = pipe.to_mir(hir)
lir = pipe.to_lir(mir)

# Direct Neural/Custom Synthesis to Bytecode
encoded = BytecodeEncoder().encode(lir)

print("=== AAYU COMPILATION SUCCESS ===")
print(f"Total Bytecode Size: {len(encoded.bytecode)} Bytes")

print("\n=== RAW HEX DUMP (Just like paper's bare-metal hex) ===")
hex_dump = " ".join([f"{b:02X}" for b in encoded.bytecode])
print(hex_dump)
