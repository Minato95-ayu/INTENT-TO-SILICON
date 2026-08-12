import sys
sys.path.append("d:/intent-to-silicon-research/INTENT-TO-SILICON")

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.type_pass import TypePass
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.errors import DiagnosticEngine

source = """
struct User {
    name: String
    age: Int
}

state user = User {
    name: "Ayush",
    age: 21
}

action update_user {
    user.age = 22
}
"""

engine = DiagnosticEngine()
lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

if engine.has_errors():
    print("Parser errors:")
    for err in engine.diagnostics:
        print(err.message)
    sys.exit(1)

scope_pass = ScopePass(engine)
scope_pass.run(ast)

if engine.has_errors():
    print("Scope errors:")
    for err in engine.diagnostics:
        print(err.message)
    sys.exit(1)
    
type_pass = TypePass(engine, scope_pass)
type_pass.run(ast)

if engine.has_errors():
    print("Type errors:")
    for err in engine.diagnostics:
        print(err.message)
    sys.exit(1)

# Pass ScopePass as it has node_types set by TypePass
hir_builder = HIRBuilder(scope_pass)
hir_builder.node_types = type_pass.node_types
hir = hir_builder.build(ast)

mir_builder = MIRBuilder()
mir = mir_builder.build(hir)

print("HIR and MIR built successfully!")
print(hir)
print(mir)
