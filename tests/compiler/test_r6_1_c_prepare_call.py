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
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.instructions import Opcode

def compile_source(source: str):
    lexer = Lexer(source)
    ast = Parser(lexer.tokenize()).parse()
    analyzer = SemanticAnalyzer()
    sem_ast = analyzer.analyze(ast)
    pipeline = IRPipeline()
    hir = pipeline.to_hir(sem_ast)
    mir = pipeline.to_mir(hir)
    lir = pipeline.to_lir(mir)
    encoder = BytecodeEncoder()
    return encoder.encode(lir)

class TestR61CPrepareCall(unittest.TestCase):
    def test_1_opcode_existence(self):
        self.assertEqual(Opcode.PREPARE_CALL, 0x2D)
        self.assertEqual(Opcode.CMP_GTE, 0x2C)
        self.assertEqual(Opcode.CALL, 0x22)
        
    def test_2_zero_argument_call(self):
        source = 'action foo() \n return 1 \n end \n foo()'
        prog = compile_source(source)
        bytecode = prog.bytecode
        found = False
        for i in range(0, len(bytecode), 3):
            if bytecode[i] == Opcode.PREPARE_CALL:
                self.assertTrue(i + 3 < len(bytecode), "Truncated bytecode after PREPARE_CALL")
                self.assertEqual(bytecode[i+1], 0)
                self.assertEqual(bytecode[i+2], 1)
                self.assertEqual(bytecode[i+3], Opcode.CALL)
                found = True
        self.assertTrue(found)
        
    def test_3_multi_argument_call(self):
        source = 'action foo(a, b) \n return a + b \n end \n foo(1, 2)'
        prog = compile_source(source)
        bytecode = prog.bytecode
        found = False
        for i in range(0, len(bytecode), 3):
            if bytecode[i] == Opcode.PREPARE_CALL:
                self.assertTrue(i + 3 < len(bytecode), "Truncated bytecode after PREPARE_CALL")
                self.assertEqual(bytecode[i+1], 2)
                self.assertEqual(bytecode[i+2], 1)
                self.assertEqual(bytecode[i+3], Opcode.CALL)
                found = True
        self.assertTrue(found)

    def test_5_call_component_isolation(self):
        source = 'component MyCard() \n Text("hello") \n end \n MyCard()'
        prog = compile_source(source)
        bytecode = prog.bytecode
        for i in range(0, len(bytecode), 3):
            if bytecode[i] == Opcode.CALL_COMPONENT:
                if i >= 3:
                    self.assertNotEqual(bytecode[i-3], Opcode.PREPARE_CALL)
                    
if __name__ == '__main__':
    unittest.main()
