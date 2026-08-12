import sys
sys.path.append("d:/intent-to-silicon-research/INTENT-TO-SILICON")

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.scope_pass import ScopePass
from aayu.compiler.semantic.type_pass import TypePass
from aayu.compiler.hir.builder import HIRBuilder
from aayu.compiler.mir.builder import MIRBuilder
from aayu.compiler.machine_lir.lowering import MachineLIRLowering
from aayu.compiler.machine_lir.nodes import MachineModule
from aayu.compiler.backend.llvm.lowering import LLVMBackend
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
"""

engine = DiagnosticEngine()
lexer = Lexer(source)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

scope_pass = ScopePass(engine)
scope_pass.run(ast)
type_pass = TypePass(engine, scope_pass)
type_pass.run(ast)

hir_builder = HIRBuilder(scope_pass)
hir_builder.node_types = type_pass.node_types
hir = hir_builder.build(ast)

mir_builder = MIRBuilder()
mir = mir_builder.build(hir)

print('MIR successfully built. Struct Decls:')
print(mir.struct_decls)

mm = MachineModule()
# Pass struct decls to LLVMBackend manually
from aayu.compiler.backend.llvm.types import StructType, i8, i32, ptr
struct_ty = StructType("User", [ptr, i32], False)
mm.struct_types = [struct_ty]

backend = LLVMBackend()
artifact = backend.lower(mm)
artifact.llvm_module.struct_types = [struct_ty]

print('\nLLVM IR Output:')
print(artifact.generate().decode('utf-8'))
