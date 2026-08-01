import sys
import os

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.layout.engine import LayoutEngine
from aayu.runtime.ui.painter import Painter
from aayu.runtime.renderers.image_renderer import ImageRenderer

def generate_screenshot(source_path: str, output_path: str):
    with open(source_path, 'r') as f:
        source = f.read()
        
    lexer = Lexer(source)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    print("DEBUG: AST Statements:")
    for stmt in ast.statements:
        print(f"  {stmt}")
        
    semantic = SemanticAnalyzer()
    semantic_ast = semantic.analyze(ast)
    
    pipeline = IRPipeline()
    mir = pipeline.to_mir(pipeline.to_hir(semantic_ast))
    print("DEBUG: MIR Instructions:")
    for inst in mir:
        print(f"  {inst}")
    ir_module = pipeline.to_lir(mir)
    
    encoder = BytecodeEncoder()
    program = encoder.encode(ir_module)
    
    vm = VirtualMachine()
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)
    vm.execute()
    
    vm.call_action_by_name("__PAGE_START__")
    tree = vm.interpreter.render_tree
    
    from aayu.runtime.ui.style_resolver import StyleResolver
    style_resolver = StyleResolver()
    
    if tree.root:
        style_resolver.resolve(tree.root)
        layout_engine = LayoutEngine(800, 600)
        layout_root = layout_engine.calculate_layout(tree.root)
        
        painter = Painter()
        display_list = painter.paint(layout_root)
        print(f"DEBUG: DisplayList items: {len(display_list.commands)}")
    else:
        print("DEBUG: tree.root is None")
        from aayu.runtime.ui.display_list import DisplayList
        display_list = DisplayList()
    
    renderer = ImageRenderer(800, 600, output_path)
    renderer.initialize()
    renderer.render(display_list)

if __name__ == "__main__":
    generate_screenshot(sys.argv[1], sys.argv[2])
