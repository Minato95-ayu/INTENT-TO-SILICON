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
tests.compiler.test_r4_3_backend — R4.3 End-to-End Backend Tests
================================================================

Verifies that the full SSA pipeline (CFG → SSA → Optimize → Linearize →
Bytecode → VM) produces correct output for fundamental AAYU programs.

These tests were the first to prove the new pipeline can execute real code.
"""

import unittest

from tests.compiler.test_helpers import CompilerE2EMixin


class TestR4_3_Backend(CompilerE2EMixin, unittest.TestCase):
    """End-to-end tests for the R4.3 backend pipeline."""

    def test_end_to_end_if_else(self):
        """Verify if/else branch selection through the full pipeline."""
        code = """
        let x = 10
        if true
            x = 20
        else
            x = 30
        end
        print(x)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("20", out)

    def test_end_to_end_optimized_math(self):
        """Verify constant folding through the full pipeline: 10 + 20 + 30 = 60."""
        code = """
        let x = 10 + 20 + 30
        print(x)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("60", out)


if __name__ == '__main__':
    unittest.main()
