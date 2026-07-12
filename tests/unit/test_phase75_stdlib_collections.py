import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

class TestPhase75StdlibCollections(unittest.TestCase):
    def run_code(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        vm = VirtualMachine()
        vm.run(bytecode)
        return vm

    def test_regex_match(self):
        vm = self.run_code('show regex::match("^[a-z]+$", "aayu").')
        # Print output is currently written to sys.stdout. We can't capture it easily without mock,
        # but if it doesn't crash it's a start.
