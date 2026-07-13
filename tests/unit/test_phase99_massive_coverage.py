import unittest
import os
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine
import sys
from io import StringIO

class TestMassiveCoverage(unittest.TestCase):
    def test_massive_coverage(self):
        source = """
        project MassiveCoverage.
        
        task main.
            let s: String = "hello".
            let l: List = [1, 2, 3].
            let m: Map = {"a": 1, "b": 2}.
            
            let b4: Boolean = 5 >= 3.
            let b5: Boolean = 2 <= 4.
            let b6: Boolean = 1 != 2.
            let b7: Boolean = 1 == 1.
            let b8: Boolean = 5 < 10.
            let b9: Boolean = 10 > 5.
            
            core::print("Coverage Check").
        end.
        run main.
        """
        
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename="<test>")
        ast = parser.parse()
        compiler = AAYUCompiler()
        compiler.compile(ast)
        
        vm = VirtualMachine()
        
        stdout = StringIO()
        sys.stdout = stdout
        try:
            vm.run(compiler.bytecode)
        finally:
            sys.stdout = sys.__stdout__
            
        self.assertIn("Coverage Check", stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
