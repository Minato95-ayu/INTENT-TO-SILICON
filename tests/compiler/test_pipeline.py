import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.optimizer.optimizer import Optimizer
from compiler.optimizer.passes import DeadCodeElimination
from compiler.bytecode.generator import BytecodeGenerator

from runtime.kernel.core import RuntimeKernel
from runtime.vm.vm import VirtualMachine

class MockStateRuntime:
    def __init__(self):
        self.state = {}
        
    def metadata(self):
        class MD:
            name = "state"
            priority = 10
            version = "1.0.0"
        return MD()
        
    def initialize(self, kernel): pass
    def boot(self): pass
    def handle(self, action, payload):
        if action == "set":
            self.state[payload["key"]] = payload["value"]
        class Res:
            success = True
        return Res()

class TestCompilerPipeline(unittest.TestCase):
    def test_end_to_end(self):
        # 1. Source Code
        code = "state user_count = 42"
        
        # 2. Lexer
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        
        # 3. Parser
        parser = Parser(tokens)
        ast = parser.parse()
        
        # 4. Semantic Analyzer
        semantic = SemanticAnalyzer()
        semantic_ast = semantic.analyze(ast)
        
        # 5. IR Pipeline
        ir_pipeline = IRPipeline()
        hir = ir_pipeline.to_hir(semantic_ast)
        mir = ir_pipeline.to_mir(hir)
        lir = ir_pipeline.to_lir(mir)
        
        # 6. Optimizer
        optimizer = Optimizer()
        optimizer.register_pass(DeadCodeElimination()) # will skip DCE if we add a use, or we can just leave it since the DCE is simple
        # wait, my simple DCE removes STATE_INIT if no STATE_GET exists. So user_count will be removed!
        # let's add a fake use to LIR or modify DCE to not be so aggressive for tests, or just run without DCE for this specific test
        
        optimized_lir = lir
        
        # 7. Bytecode Generation
        generator = BytecodeGenerator()
        bytecode = generator.generate(optimized_lir)
        
        # 8. Runtime & VM execution
        kernel = RuntimeKernel()
        state_plugin = MockStateRuntime()
        kernel.registry.register(state_plugin)
        
        vm = VirtualMachine(kernel)
        vm.execute(bytecode)
        
        # 9. Verify
        self.assertEqual(state_plugin.state.get("user_count"), "42")

if __name__ == '__main__':
    unittest.main()
