from aayu.runtime.vm.vm import VirtualMachine
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.runtime.session.manager import SessionManager
import json

with open("../test.aayu", "r") as f:
    src = f.read()

tokens = Lexer(src).tokenize()
ast = Parser(tokens).parse()
ast = SemanticAnalyzer().analyze(ast)

pipeline = IRPipeline()
hir = pipeline.to_hir(ast)
mir = pipeline.to_mir(hir)
lir = pipeline.to_lir(mir)
prog = BytecodeEncoder().encode(lir)

manager = SessionManager(prog)
session = manager.get_or_create_session(None)

from aayu.runtime.renderers.web_renderer import serialize_node
style_sheet = set()
print("Initial JSON:", serialize_node(session.vm.interpreter.render_tree.root, style_sheet))
print("State:", session.vm.state)

session.vm.call_action_by_name("increment")
# Force execute since manager event loop isn't running here
session.vm.execute()

style_sheet = set()
print("After increment action:")
print("State:", session.vm.state)

session.vm.call_action_by_name("__PAGE_START__")
session.vm.execute()

style_sheet = set()
print("After PAGE_START:")
print("JSON:", serialize_node(session.vm.interpreter.render_tree.root, style_sheet))
print("State:", session.vm.state)

