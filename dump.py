import sys
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder

source_code = """
route "/api/v1/compile"
    post
        let req = request.body
        let code = req["code"]
    end
end
"""
tokens = Lexer(source_code).tokenize()
ast = Parser(tokens).parse()
semantic_ast = SemanticAnalyzer().analyze(ast)
ir_pipeline = IRPipeline()
lir = ir_pipeline.to_lir(ir_pipeline.to_mir(ir_pipeline.to_hir(semantic_ast)))
prog = BytecodeEncoder().encode(lir)
print(list(prog.bytecode))
