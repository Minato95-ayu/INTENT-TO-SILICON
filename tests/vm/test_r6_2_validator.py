import unittest
from runtime.vm.exceptions import InvalidBytecodeError
from runtime.vm.validator import Validator
from runtime.vm.instructions import Opcode

class TestR62Validator(unittest.TestCase):
    def test_truncated_instruction(self):
        bytecode = bytearray([Opcode.PUSH_CONST, 0]) # only 2 bytes
        with self.assertRaisesRegex(InvalidBytecodeError, "not a multiple of 3"):
            Validator.validate(bytecode, [])

    def test_jump_into_middle_of_instruction(self):
        bytecode = bytearray([
            Opcode.JMP, 0, 4, # target is 4, which is in the middle of next instruction
            Opcode.PUSH_CONST, 0, 0,
            Opcode.HALT, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Jump target inside operand"):
            Validator.validate(bytecode, [])

    def test_call_without_prepare_call(self):
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0,
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            Opcode.RETURN_VALUE, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Naked CALL without PREPARE_CALL"):
            Validator.validate(bytecode, [])

    def test_prepare_call_without_immediate_call(self):
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 0, 0,
            Opcode.PUSH_CONST, 0, 0,
            Opcode.CALL, 0, 12,
            Opcode.HALT, 0, 0,
            Opcode.RETURN_VALUE, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "PREPARE_CALL must be immediately followed by CALL"):
            Validator.validate(bytecode, [])

    def test_call_with_insufficient_stack_depth(self):
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 1, 0,
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            Opcode.POP, 0, 0,
            Opcode.RET, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Stack underflow"):
            Validator.validate(bytecode, [])

    def test_invalid_call_target(self):
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 0, 0,
            Opcode.CALL, 0, 12,
            Opcode.HALT, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Jump target inside operand"):
            Validator.validate(bytecode, [])

    def test_build_widget_stack_underflow(self):
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0, 
            Opcode.BUILD_WIDGET, 0, 1,
            Opcode.HALT, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Stack underflow"):
            Validator.validate(bytecode, [])

    def test_wrong_return_value_depth(self):
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 0, 0,
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            # Subroutine expects 0 returns
            Opcode.PUSH_CONST, 0, 0,
            Opcode.RETURN_VALUE, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "RETURN_VALUE used but expected 0 returns"):
            Validator.validate(bytecode, [])
            
        bytecode2 = bytearray([
            Opcode.PREPARE_CALL, 0, 1,
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.PUSH_CONST, 0, 2,
            Opcode.RETURN_VALUE, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Stack depth mismatch on RETURN_VALUE: expected 1, got 2"):
            Validator.validate(bytecode2, [])

    def test_wrong_ret_depth(self):
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 0, 0,
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.RET, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Stack depth mismatch on RET: expected 0, got 1"):
            Validator.validate(bytecode, [])

    def test_branch_paths_incompatible_stack_depths(self):
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 1,
            Opcode.JMP_IF_FALSE, 0, 12,
            Opcode.PUSH_CONST, 0, 2,
            Opcode.JMP, 0, 18,
            # false path (IP 12)
            Opcode.PUSH_CONST, 0, 3,
            Opcode.PUSH_CONST, 0, 4,
            # merge point (IP 18)
            Opcode.HALT, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Incompatible stack depths at merge point"):
            Validator.validate(bytecode, [])

if __name__ == '__main__':
    unittest.main()
