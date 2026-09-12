import unittest
from runtime.vm.instructions import Opcode, opcode_to_str

class TestVMInstructions(unittest.TestCase):
    def test_instructions(self):
        for k, v in Opcode.__dict__.items():
            if not k.startswith("__"):
                self.assertEqual(opcode_to_str(v), k)
