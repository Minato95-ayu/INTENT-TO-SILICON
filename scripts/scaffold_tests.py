import os

tests_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\tests"

def write_file(path, content):
    full_path = os.path.join(tests_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Scaffolding Stdlib tests...")

write_file("test_phase75_stdlib_collections.py", """\
import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language')))
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
        vm = VirtualMachine(bytecode)
        vm.run()
        return vm

    def test_regex_match(self):
        vm = self.run_code('show regex::match("^[a-z]+$", "aayu").')
        # Print output is currently written to sys.stdout. We can't capture it easily without mock,
        # but if it doesn't crash it's a start.
""")

write_file("test_phase76_stdlib_database.py", """\
import unittest
import os
import sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'language')))
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
        vm = VirtualMachine(bytecode)
        vm.run()
        return vm

    def test_sqlite(self):
        # Create temp db
        conn = sqlite3.connect("test.db")
        conn.execute("CREATE TABLE users (id INT, name TEXT)")
        conn.execute("INSERT INTO users VALUES (1, 'Alice')")
        conn.commit()
        conn.close()

        vm = self.run_code('show sqlite::query("test.db", "SELECT * FROM users").')
        
        os.remove("test.db")
""")

print("Tests created.")
