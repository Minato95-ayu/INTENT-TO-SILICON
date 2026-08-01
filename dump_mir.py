from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline

source = open('ecommerce.aayu').read()
l = Lexer(source)
ast = Parser(l.tokenize()).parse()
ast = SemanticAnalyzer().analyze(ast)
pipe = IRPipeline()
hir = pipe.to_hir(ast)
mir = pipe.to_mir(hir)

# Print MIR instructions
for m in mir:
    if hasattr(m, 'opcode'):
        if m.opcode == "ACTION_DECL":
            name = m.operands[0]
            body = m.operands[1]
            print(f"\n=== ACTION: {name} ===")
            for b in body:
                print(f"  {b.opcode} {b.operands}")
        else:
            print(f"{m.opcode} {m.operands}")
