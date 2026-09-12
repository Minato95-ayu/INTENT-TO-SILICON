import unittest
from runtime.vm.vm import VirtualMachine
from runtime.vm.instructions import Opcode
from runtime.vm.exceptions import InvalidBytecodeError, RuntimeException

class TestR61CRuntimeABI(unittest.TestCase):
    def setUp(self):
        self.vm = VirtualMachine()

    def test_valid_call_and_return(self):
        # Caller: PREPARE_CALL 1, 1; CALL target
        # Callee: RETURN_VALUE
        bytecode = bytearray([
            # 0: push arg
            Opcode.PUSH_CONST, 0, 0,
            # 3: PREPARE_CALL 1, 1
            Opcode.PREPARE_CALL, 1, 1,
            # 6: CALL target (ip 12)
            Opcode.CALL, 0, 12,
            # 9: HALT
            Opcode.HALT, 0, 0,
            # 12: TARGET: pop arg, return a dummy value
            Opcode.POP, 0, 0,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.RETURN_VALUE, 0, 0
        ])
        constant_pool = [10, 20]
        try:
            self.vm.load(bytecode, constant_pool)
            self.vm.execute()
            self.assertEqual(self.vm.value_stack.depth(), 1)
        except Exception as e:
            self.fail(f"Valid execution failed: {e}")

    def test_return_too_many_values_rejected(self):
        # Caller expects 1 return, callee pushes 2 values then RETURN_VALUE
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0,
            Opcode.PREPARE_CALL, 1, 1,
            Opcode.CALL, 0, 12,
            Opcode.HALT, 0, 0,
            
            # TARGET: pop arg
            Opcode.POP, 0, 0,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.RETURN_VALUE, 0, 0
        ])
        constant_pool = [10, 20]
        
        with self.assertRaisesRegex(Exception, "Stack depth mismatch on (RETURN_VALUE|RET): expected 1, got 2"):
            self.vm.load(bytecode, constant_pool)
            self.vm.execute()

    def test_return_too_few_values_rejected(self):
        # Caller expects 1 return, callee pushes 0 values then RETURN_VALUE
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0,
            Opcode.PREPARE_CALL, 1, 1,
            Opcode.CALL, 0, 12,
            Opcode.HALT, 0, 0,
            
            # TARGET: pop arg, don't push anything, just return
            Opcode.POP, 0, 0,
            Opcode.RETURN_VALUE, 0, 0
        ])
        constant_pool = [10, 20]
        
        with self.assertRaisesRegex(Exception, "Stack depth mismatch on (RETURN_VALUE|RET): expected 1, got 0"):
            self.vm.load(bytecode, constant_pool)
            self.vm.execute()

    def test_naked_call_rejected(self):
        # CALL without preceding PREPARE_CALL
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0,
            # NO PREPARE CALL!
            Opcode.CALL, 0, 9,
            Opcode.HALT, 0, 0,
            
            # TARGET
            Opcode.POP, 0, 0,
            Opcode.RETURN_VALUE, 0, 0
        ])
        constant_pool = [10]
        
        with self.assertRaisesRegex(Exception, "Naked CALL without PREPARE_CALL"):
            # The validator should actually catch this first! Let's bypass validator.
            self.vm.load(bytecode, constant_pool)
            # execute via interpreter directly to bypass validator
            self.vm.interpreter.execute()

    def test_ret_too_many_values_rejected(self):
        # Caller expects 0 returns, callee pushes 1 value then RET
        bytecode = bytearray([
            Opcode.PUSH_CONST, 0, 0,
            Opcode.PREPARE_CALL, 1, 0,
            Opcode.CALL, 0, 12,
            Opcode.HALT, 0, 0,
            
            # TARGET
            Opcode.POP, 0, 0,
            Opcode.PUSH_CONST, 0, 1,
            Opcode.RET, 0, 0
        ])
        constant_pool = [10, 20]
        
        with self.assertRaisesRegex(Exception, "Stack depth mismatch on (RETURN_VALUE|RET): expected 0, got 1"):
            self.vm.load(bytecode, constant_pool)
            self.vm.execute()

if __name__ == '__main__':
    unittest.main()
