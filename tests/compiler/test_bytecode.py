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

import unittest
from compiler.ir.lir import LIRNode
from compiler.bytecode.generator import BytecodeGenerator

class TestBytecodeGenerator(unittest.TestCase):
    def test_generate_bytecode(self):
        lir = [
            LIRNode("STATE_INIT", ["counter", "0"]),
            LIRNode("BUILD_PAGE", ["Home"]),
        ]
        
        generator = BytecodeGenerator()
        bytecode = generator.generate(lir)
        
        self.assertEqual(len(bytecode.instructions), 2)
        
        self.assertEqual(bytecode.instructions[0].opcode, "STATE_INIT")
        self.assertEqual(bytecode.instructions[0].arg1, "counter")
        self.assertEqual(bytecode.instructions[0].arg2, "0")
        
        self.assertEqual(bytecode.instructions[1].opcode, "BUILD_PAGE")
        self.assertEqual(bytecode.instructions[1].arg1, "Home")

if __name__ == '__main__':
    unittest.main()
