"""
tests.compiler.test_r4_4_backend_hardening — R4.4 Backend Hardening Tests
=========================================================================

Exercises edge cases in the backend pipeline:
- Nested control flow (if inside if)
- Parallel PHI copies (multiple variables diverge/merge)
- Unreachable code after return
"""

import unittest

from tests.compiler.test_helpers import CompilerE2EMixin


class TestR4_4_BackendHardening(CompilerE2EMixin, unittest.TestCase):
    """Hardening tests for complex backend lowering scenarios."""

    def test_nested_control_flow(self):
        """Nested if/else: inner else branch (200) should be selected."""
        code = """
        let result = 0
        if true
            if false
                result = 100
            else
                result = 200
            end
        else
            result = 300
        end
        print(result)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("200", out)

    def test_parallel_phi_copies(self):
        """Multiple variables modified in branches must be correctly copied.

        Both x and y are reassigned in if/else.  At the merge point,
        two PHI nodes are needed — the Linearizer must insert two COPY
        instructions in each predecessor without clobbering.
        """
        code = """
        let x = 10
        let y = 20
        if false
            x = 100
            y = 200
        else
            x = 1000
            y = 2000
        end
        let total = x + y
        print(total)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("3000", out)

    def test_unreachable_blocks(self):
        """Code after a return should be silently discarded, not crash."""
        code = """
        action test()
            return 42
            print(999)
        end
        let a = test()
        print(a)
        """
        out = self.execute_aayu(code, use_ssa=True)
        self.assertIn("42", out)
        self.assertNotIn("999", out)


if __name__ == '__main__':
    unittest.main()
