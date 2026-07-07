"""
=============================================================================
FILE: test_vm_collections.py
PURPOSE: Test suite for AAYU components
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles test suite for aayu components.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import sys
import unittest
import io
import contextlib

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from vm import VirtualMachine
from compiler.frontend.ir import Bytecode
from serializer import serialize, deserialize

class TestVMCollections(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)

    def test_constants_serialization(self):
        """Verify that collections in constant pools serialize and deserialize correctly."""
        bc = Bytecode()
        bc.constants = [
            [],
            {},
            ["a", "b"],
            {"name": "Ayush"},
            [{"name": "Ayush"}]
        ]
        
        # Serialize and deserialize
        serialized = serialize(bc)
        deserialized = deserialize(serialized)
        
        # Assert matching constants
        self.assertEqual(len(deserialized.constants), len(bc.constants))
        self.assertEqual(deserialized.constants[0], [])
        self.assertEqual(deserialized.constants[1], {})
        self.assertEqual(deserialized.constants[2], ["a", "b"])
        self.assertEqual(deserialized.constants[3], {"name": "Ayush"})
        self.assertEqual(deserialized.constants[4], [{"name": "Ayush"}])

    def run_vm_test_file(self, filename, expected_output):
        filepath = os.path.join(self.tests_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        
        # 1. Run VM directly
        vm = VirtualMachine()
        f_direct = io.StringIO()
        with contextlib.redirect_stdout(f_direct):
            vm.run(bytecode)
        direct_out = f_direct.getvalue().strip().replace('\r\n', '\n')
        vm.close()
        
        # 2. Serialize -> Deserialize -> Run VM
        serialized = serialize(bytecode)
        deserialized = deserialize(serialized)
        
        vm_deserialized = VirtualMachine()
        f_serialized = io.StringIO()
        with contextlib.redirect_stdout(f_serialized):
            vm_deserialized.run(deserialized)
        serialized_out = f_serialized.getvalue().strip().replace('\r\n', '\n')
        vm_deserialized.close()
        
        # Assert correctness
        self.assertEqual(direct_out, expected_output.strip().replace('\r\n', '\n'))
        self.assertEqual(serialized_out, expected_output.strip().replace('\r\n', '\n'))


    def test_vm_list(self):
        expected = """['Learn VM', 'Build Runtime']
Learn VM
Build Runtime"""
        self.run_vm_test_file("vm_list.aayu", expected)

    def test_vm_map(self):
        expected = """{'name': 'Ayush', 'age': 20.0}
Ayush
20.0"""
        self.run_vm_test_file("vm_map.aayu", expected)

    def test_vm_nested_map(self):
        expected = "[{'name': 'Ayush'}]"
        self.run_vm_test_file("vm_nested_map.aayu", expected)

    def test_vm_map_lookup(self):
        expected = "Ayush"
        self.run_vm_test_file("vm_map_lookup.aayu", expected)

if __name__ == "__main__":
    unittest.main()
