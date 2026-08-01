import sys
import os

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder

from aayu.runtime.vm.vm import VirtualMachine

def main():
    with open("test_navigation.aayu", "r") as f:
        code = f.read()
        
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    
    parser = Parser(tokens)
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    semantic_ast = analyzer.analyze(ast)
    
    ir_pipeline = IRPipeline()
    lir = ir_pipeline.to_lir(ir_pipeline.to_mir(ir_pipeline.to_hir(semantic_ast)))
    
    encoder = BytecodeEncoder()
    program = encoder.encode(lir)
    
    from aayu.runtime.vm.decoder import Decoder
    from aayu.runtime.vm.instructions import Opcode, opcode_to_str
    
    print("\n--- Disassembly ---")
    d = Decoder(program.bytecode, program.constant_pool.values())
    ip = 0
    while ip < len(program.bytecode):
        op = d.fetch8(ip)
        arg = d.fetch16(ip + 1)
        if op == Opcode.HALT:
            print(f"{ip:04d}: HALT")
            break
        else:
            print(f"{ip:04d}: {opcode_to_str(op)} {arg}")
        ip += 3
    print("-------------------\n")
    
    vm = VirtualMachine()
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)
    vm.call_action_by_name("__PAGE_START__")
    vm.execute()
    
    def print_tree(node, indent=0):
        print("  " * indent + f"{node.type} {node.props}")
        for child in node.children:
            print_tree(child, indent + 1)
            
    print("Initial Tree:")
    print_tree(vm.interpreter.render_tree.root)
    
    # Let's trigger a button click to navigate
    # We find the navigate action name
    action_name = None
    for k in vm.state_scopes_map:
        print("Scope:", k, vm.state_scopes_map[k])
    
    # We simulate a navigation
    vm.router.navigate("Profile", {"id": 42, "name": "Ayush"})
    if vm.router.current_route:
        instance_id = f"page_{vm.router.current_route.name}"
        if instance_id not in vm.state_scopes_map:
            vm.state_scopes_map[instance_id] = {"__instance_id__": instance_id}
        
        for k, v in vm.router.current_route.params.items():
            vm.state_scopes_map[instance_id][k] = v
            
        vm.state_scopes.append(vm.state_scopes_map[instance_id])
        
        vm.call_action_by_name(f"__PAGE_START_{vm.router.current_route.name}")
        vm.execute()
        
        vm.state_scopes.pop()
    
    print("\nTree after navigation:")
    print_tree(vm.interpreter.render_tree.root)

if __name__ == "__main__":
    main()
