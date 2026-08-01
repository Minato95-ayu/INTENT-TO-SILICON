from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.session.manager import SessionManager

code = """
Page PageA
    Icon name="store"
end
Page PageB
    Icon name="user-circle"
end
"""
tokens = Lexer(code).tokenize()
ast = SemanticAnalyzer().analyze(Parser(tokens).parse())
pipeline = IRPipeline()
prog = BytecodeEncoder().encode(pipeline.to_lir(pipeline.to_mir(pipeline.to_hir(ast))))

vm = SessionManager(prog).get_or_create_session("test").vm
vm.call_action_by_name("PageA")
print(f"Stack size after PageA: {vm.value_stack.depth}")
vm.call_action_by_name("PageB")
print(f"Stack size after PageB: {vm.value_stack.depth}")
