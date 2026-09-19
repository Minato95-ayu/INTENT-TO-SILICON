# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import pytest
pytestmark = pytest.mark.skip(reason='Obsolete API: AAYUCompiler removed in favor of IRPipeline')

import unittest
import os
import sys
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
# # from compiler.frontend.compiler import AAYUCompiler
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

        vm = self.run_code('show db::query("test.db", "SELECT * FROM users").')
        
        os.remove("test.db")
