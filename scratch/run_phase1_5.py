import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

# 1. Compile
with open("scratch/test_phase1_5.aayu", "r") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

analyzer = SemanticAnalyzer()
semantic_tree = analyzer.analyze(ast)

pipeline = IRPipeline()
hir = pipeline.to_hir(semantic_tree)
mir = pipeline.to_mir(hir)
lir = pipeline.to_lir(mir)

encoder = BytecodeEncoder()
program = encoder.encode(lir)

print(f"Compilation Successful: {len(program.bytecode)} bytes")

# 2. Execute
vm = VirtualMachine()
vm.load(program.bytecode, program.constant_pool, program.action_addresses)
vm.call_action_by_name("__PAGE_START_Home")
vm.execute()
print("Execution Completed successfully!")
print("Node Stack Depth:", len(vm.interpreter.node_stack))
if vm.interpreter.render_tree.root:
    def print_node(node, indent=""):
        props = getattr(node, 'props', {})
        print(f"{indent}{node.type} {props}")
        # Look for bindings, validations, animations
        # Wait, they are stored in `children` array during node_stack construction if they were tuples
        # But during MARK_BLOCK_END, do they get attached to props? Let's see!
        for c in node.children:
            if isinstance(c, tuple):
                print(f"{indent}  *{c[0]} -> {c[1]}")
            elif isinstance(c, str):
                print(f"{indent}  '{c}'")
            else:
                print_node(c, indent + "  ")
    print_node(vm.interpreter.render_tree.root)

