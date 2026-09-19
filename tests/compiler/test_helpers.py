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

"""
tests.compiler.test_helpers — shared test infrastructure for compiler E2E tests
===============================================================================

Provides ``CompilerE2EMixin``, a mixin class that compiles AAYU source code
through the full pipeline (Lex → Parse → Semantic → CFG → SSA → Optimize →
Linearize → Bytecode → VM) and captures the program output.

VM trace lines (``[VM TRACE]``, ``[VM]``, ``[SessionManager]``,
``[DEBUG ENCODER]``) are automatically filtered out so that assertions
match only actual program output.
"""

import sys
import io

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.ir.optimizer import SSAOptimizer
from compiler.ir.linearizer import Linearizer
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.session.manager import SessionManager


# Prefixes emitted by the VM / encoder debug tracing.
_TRACE_PREFIXES = (
    "[VM TRACE]",
    "[VM]",
    "[SessionManager]",
    "[DEBUG ENCODER]",
)


class CompilerE2EMixin:
    """Mixin for test classes that need full pipeline E2E execution.

    Usage::

        class TestMyFeature(CompilerE2EMixin, unittest.TestCase):
            def test_something(self):
                lines = self.execute_aayu(\"\"\"
                    let x = 42
                    print(x)
                \"\"\")
                self.assertIn("42", lines)
    """

    def execute_aayu(self, code: str, use_ssa: bool = False) -> list[str]:
        """Compile and execute AAYU source code, returning output lines.

        Parameters
        ----------
        code : str
            AAYU source code to compile and run.
        use_ssa : bool
            Whether to use the experimental SSA/CFG pipeline (default False).

        Returns
        -------
        list[str]
            Lines of program output, with VM debug traces filtered out.
        """
        # Compile through the full pipeline.
        lexer = Lexer(code)
        ast = Parser(lexer.tokenize()).parse()
        semantic_ast = SemanticAnalyzer().analyze(ast)

        pipeline = IRPipeline()
        if use_ssa:
            cfg = pipeline.to_ssa_cfg(semantic_ast)
            SSAOptimizer(cfg).optimize()
            mir = Linearizer(cfg).lower()
        else:
            hir = pipeline.to_hir(semantic_ast)
            mir = pipeline.to_mir(hir)
            
        lir = pipeline.to_lir(mir)
        prog = BytecodeEncoder().encode(lir)

        # Execute on the VM, capturing stdout.
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            manager = SessionManager(prog)
            session = manager.get_or_create_session("test-session")
            session.vm.execute()
            raw_output = sys.stdout.getvalue()
        finally:
            if 'session' in locals():
                session.shutdown()
            sys.stdout = old_stdout

        # Filter out VM trace / debug lines.
        lines = raw_output.strip().split('\n')
        return [line for line in lines
                if not any(line.startswith(prefix)
                           for prefix in _TRACE_PREFIXES)]
