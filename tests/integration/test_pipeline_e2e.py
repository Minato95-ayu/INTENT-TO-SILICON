import unittest
import os
import shutil
import tempfile
from intent_engine.v2.engine import IntentEngine
from brainos.v2.generator import ProjectGenerator
from tools.cli_formatter import AAYUFormatter
from tools.cli_linter import AAYULinter
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

class TestPipelineE2E(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.project_dir = os.path.join(self.temp_dir, "e2e_test")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_full_autonomous_pipeline(self):
        prompt = "Create a simple calculator"
        
        # 1. Intent Engine
        engine = IntentEngine()
        intent = engine.process_prompt(prompt)
        self.assertIn("actions", intent)
        
        # 2. Generator
        generator = ProjectGenerator(target_dir=self.temp_dir)
        success = generator.generate(prompt, project_name="e2e_test")
        self.assertTrue(success)
        
        main_aayu = os.path.join(self.project_dir, "src", "main.aayu")
        self.assertTrue(os.path.exists(main_aayu))
        
        with open(main_aayu, "r") as f:
            code = f.read()
            
        # 3. Formatter
        formatter = AAYUFormatter()
        formatted_code = formatter.format(code)
        self.assertTrue(len(formatted_code) > 0)
        
        # 4. Linter
        linter = AAYULinter()
        diagnostics = linter.lint(formatted_code)
        self.assertEqual(len(diagnostics), 0, f"Lint errors: {diagnostics}")
        
        # 5. Compiler
        lexer = Lexer(formatted_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, filename="<test>")
        ast = parser.parse()
        compiler = AAYUCompiler(filename="<test>")
        bytecode = compiler.compile(ast)
        self.assertTrue(len(bytecode.instructions) > 0)
        
        # 6. VM
        vm = VirtualMachine()
        vm.run(bytecode)
        
        # If it runs without raising exception, test passes.
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
