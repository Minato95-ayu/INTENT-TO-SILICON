import unittest
import os
import sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

class TestPhase76StdlibDatabase(unittest.TestCase):
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

    def test_sqlite(self):
        import os
        if os.path.exists("test.db"): os.remove("test.db")
        # Create temp db
        conn = sqlite3.connect("test.db")
        conn.execute("CREATE TABLE users (id INT, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        conn.commit()
        conn.close()

        vm = self.run_code('show sqlite::query("test.db", "SELECT * FROM users").')
        
        os.remove("test.db")
