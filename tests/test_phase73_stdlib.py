"""
=============================================================================
FILE: test_phase73_stdlib.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import unittest
import os
import sys

# Add prototype/language to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..')))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine

class TestPhase73Stdlib(unittest.TestCase):
    def run_code(self, code: str):
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        compiler = AAYUCompiler()
        bc = compiler.compile(ast)
        vm = VirtualMachine(trace_execution=False)
        vm.run(bc)
        return vm.output

    def test_core_print(self):
        code = '''
        function main()
            core::print("hello from core").
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output[-1], "hello from core")

    def test_math_functions(self):
        code = '''
        function main()
            let x is math::sqrt(16).
            let y is math::pow(2, 3).
            let z is math::abs(-10).
            let m1 is math::min(5, 10).
            let m2 is math::max(5, 10).
            let f is math::floor(3.7).
            let c is math::ceil(3.2).
            let r is math::round(3.5).
            print(x).
            print(y).
            print(z).
            print(m1).
            print(m2).
            print(f).
            print(c).
            print(r).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["4.0", "8.0", "10.0", "5.0", "10.0", "3.0", "4.0", "4.0"])

    def test_string_functions(self):
        code = '''
        function main()
            let s is "hello world".
            let parts is string::split(s, " ").
            let up is string::upper(s).
            let trim is string::trim("  hey  ").
            let rep is string::replace(s, "world", "aayu").
            let contains is string::contains(s, "lo").
            print(string::length(parts)).
            print(up).
            print(trim).
            print(rep).
            print(contains).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["2.0", "HELLO WORLD", "hey", "hello aayu", "true"])

    def test_list_functions(self):
        code = '''
        function main()
            let lst is [1, 2, 3].
            list::push(lst, 4).
            let popped is list::pop(lst).
            list::insert(lst, 0, 9).
            list::remove(lst, 1).
            list::reverse(lst).
            list::sort(lst).
            print(list::length(lst)).
            print(popped).
            print(list::get(lst, 0)).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["3.0", "4.0", "2.0"])

    def test_map_functions(self):
        code = '''
        function main()
            let m is { "a": 1 }.
            map::put(m, "b", 2).
            let val is map::get(m, "b").
            let has_a is map::contains(m, "a").
            map::remove(m, "a").
            let has_a_after is map::contains(m, "a").
            print(val).
            print(has_a).
            print(has_a_after).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["2.0", "true", "false"])

    def test_file_functions(self):
        code = '''
        function main()
            let path is "test_file_stdlib.txt".
            file::write(path, "test_data").
            file::append(path, "_appended").
            let data is file::read(path).
            let ex is file::exists(path).
            file::delete(path).
            let ex2 is file::exists(path).
            print(data).
            print(ex).
            print(ex2).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["test_data_appended", "true", "false"])

    def test_json_functions(self):
        code = '''
        function main()
            let obj is { "key": "value", "arr": [1, 2] }.
            let s is json::encode(obj).
            let dec is json::decode(s).
            let val is map::get(dec, "key").
            print(val).
        end.
        run main.
        '''
        output = self.run_code(code)
        self.assertEqual(output, ["value"])

if __name__ == '__main__':
    unittest.main()
