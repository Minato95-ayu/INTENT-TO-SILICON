import unittest
from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.semantic.analyzer import SemanticAnalyzer
from compiler.ir.pipeline import IRPipeline
from compiler.bytecode.encoder import BytecodeEncoder
from runtime.vm.vm import VirtualMachine
from runtime.vm.exceptions import InvalidBytecodeError
from runtime.vm.instructions import Opcode
from runtime.vm.validator import Validator

def compile_and_run(source):
    lexer = Lexer(source)
    ast = Parser(lexer.tokenize()).parse()
    analyzer = SemanticAnalyzer()
    sem_ast = analyzer.analyze(ast)
    
    pipeline = IRPipeline()
    hir = pipeline.to_hir(sem_ast)
    mir = pipeline.to_mir(hir)
    lir_nodes = pipeline.to_lir(mir)
    
    encoder = BytecodeEncoder()
    prog = encoder.encode(lir_nodes)
    pool = encoder.pool
    
    Validator.validate(prog.bytecode, pool)
    
    vm = VirtualMachine()
    # VirtualMachine load signature: load(self, bytecode, constant_pool=None, action_addresses=None, action_params=None)
    vm.load(prog.bytecode, pool, encoder._action_addresses, encoder._action_params)
    vm.execute()
    return vm

class TestR61C(unittest.TestCase):

    def test_argument_order(self):
        source = """
        action subtract(a, b)
            return a - b
        end
        let result = subtract(10, 3)
        """
        vm = compile_and_run(source)
        self.assertEqual(vm.state["result"], 7)

    def test_scope_isolation_caller_locals(self):
        source = """
        let x = 100
        action foo(x)
            x = 999
            return x
        end
        let res = foo(x)
        """
        vm = compile_and_run(source)
        self.assertEqual(vm.state["x"], 100)
        self.assertEqual(vm.state["res"], 999)

    def test_recursion_correctness(self):
        source = """
        action fib(n)
            if n < 2
                return n
            end
            return fib(n-1) + fib(n-2)
        end
        let result = fib(5)
        """
        vm = compile_and_run(source)
        self.assertEqual(vm.state["result"], 5)

    def test_zero_args_zero_returns_no_stack_leak(self):
        # We manually construct bytecode since the compiler currently defaults to returns=1
        vm = VirtualMachine()
        # PREPARE_CALL 0, 0
        # CALL 9
        # HALT
        # TARGET (offset 9) -> RET
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 0, 0, 
            Opcode.CALL, 0, 9, 
            Opcode.HALT, 0, 0, 
            Opcode.RET, 0, 0
        ])
        Validator.validate(bytecode, [])
        vm.load(bytecode, [], {}, {})
        vm.execute()
        self.assertEqual(vm.value_stack.depth(), 0)

    def test_verifier_rejects_naked_call(self):
        bytecode = bytearray([Opcode.CALL, 0x00, 0x00, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "Naked CALL without PREPARE_CALL"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_dangling_prepare(self):
        bytecode = bytearray([Opcode.PREPARE_CALL, 0, 0, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "PREPARE_CALL must be immediately followed by CALL"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_interrupted_prepare(self):
        bytecode = bytearray([Opcode.PREPARE_CALL, 0, 0, Opcode.PUSH_CONST, 0, 0, Opcode.CALL, 0, 0, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "PREPARE_CALL must be immediately followed by CALL"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_double_prepare(self):
        bytecode = bytearray([Opcode.PREPARE_CALL, 0, 0, Opcode.PREPARE_CALL, 0, 0, Opcode.CALL, 0, 0, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "PREPARE_CALL must be immediately followed by CALL"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_insufficient_stack(self):
        # target=9. subroutine at 9: STORE_STATE 0, STORE_STATE 1, RET
        bytecode = bytearray([
            Opcode.PREPARE_CALL, 2, 0, 
            Opcode.CALL, 0, 9, 
            Opcode.HALT, 0, 0, 
            Opcode.STORE_STATE, 0, 0, 
            Opcode.STORE_STATE, 0, 1, 
            Opcode.RET, 0, 0
        ])
        with self.assertRaisesRegex(InvalidBytecodeError, "Insufficient stack depth for CALL. Expected 2, got 0"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_invalid_target(self):
        bytecode = bytearray([Opcode.PREPARE_CALL, 0, 0, Opcode.CALL, 0xFF, 0xFE, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "Jump target inside operand"):
            Validator.validate(bytecode, [])

    def test_verifier_rejects_target_inside_operand(self):
        bytecode = bytearray([Opcode.PREPARE_CALL, 0, 0, Opcode.CALL, 0x00, 0x04, Opcode.PUSH_CONST, 0, 0, Opcode.HALT, 0, 0])
        with self.assertRaisesRegex(InvalidBytecodeError, "Jump target inside operand"):
            Validator.validate(bytecode, [])

if __name__ == "__main__":
    unittest.main()
