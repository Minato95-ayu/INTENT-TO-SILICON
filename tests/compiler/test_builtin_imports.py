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

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.vm import VirtualMachine


def test_builtin_import_and_namespace_call_execute():
    source = """
    import math.
    let result = math::pow(2, 3)
    print result.
    """
    ast = Parser(Lexer(source).tokenize()).parse()
    assert ast.statements[0].module == "math"
    assert ast.statements[1].value.name == "math::pow"

    semantic = SemanticAnalyzer().analyze(ast)
    pipeline = IRPipeline()
    program = BytecodeEncoder().encode(
        pipeline.to_lir(pipeline.to_mir(pipeline.to_hir(semantic)))
    )
    vm = VirtualMachine()
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)
    vm.execute()

    result = vm.state["result"]
    assert result.to_python() == 8 if hasattr(result, "to_python") else result == 8