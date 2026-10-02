import sys
import os
sys.path.insert(0, os.path.abspath("."))
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline

code = """
Page Counter
    state count = 0
    state msg = "Count is: "
    
    action inc()
        count = count + 1
        msg = "Count is: " + count
    end
    
    Column
        Text msg
        Button "Inc" onClick=inc
    end
end
"""
tokens = Lexer(code).tokenize()
ast = Parser(tokens).parse()
ast = SemanticAnalyzer().analyze(ast)
pipeline = IRPipeline()
hir = pipeline.to_hir(ast)
mir = pipeline.to_mir(hir)
for m in mir:
    if m.opcode == "DECLARE_ACTION":
        print(f"Action {m.operands[0]}")
        for b in m.operands[1]:
            print("  ", b.opcode, getattr(b, "operands", ""))
