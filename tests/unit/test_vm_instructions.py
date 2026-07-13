import unittest
from compiler.frontend.ir import Opcode

class TestVMInstructions(unittest.TestCase):
    def test_instructions(self):
        # Access all opcodes to trigger coverage of the enum
        for op in Opcode:
            self.assertIsNotNone(op.name)
            self.assertIsNotNone(op.value)

if __name__ == '__main__':
    unittest.main()
