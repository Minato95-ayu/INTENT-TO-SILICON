import unittest
from aayu.runtime.kernel.core import RuntimeKernel
from aayu.runtime.vm.vm import VirtualMachine
from aayu.compiler.bytecode.instructions import BytecodeObject, Instruction

class MockPlugin:
    def __init__(self):
        self.dispatched = []
    def metadata(self):
        class MD:
            name = "state"
            priority = 10
            version = "1.0.0"
        return MD()
    def initialize(self, kernel): pass
    def boot(self): pass
    def handle(self, action, payload):
        self.dispatched.append((action, payload))
        class Res:
            success = True
        return Res()

class TestVM(unittest.TestCase):
    def test_execute_state_init(self):
        kernel = RuntimeKernel()
        mock_state = MockPlugin()
        kernel.registry.register(mock_state)
        
        bytecode = BytecodeObject(
            instructions=[
                Instruction("STATE_INIT", "counter", "0")
            ],
            constants=[]
        )
        
        vm = VirtualMachine(kernel)
        vm.execute(bytecode)
        
        # Verify it dispatched to the kernel
        self.assertEqual(len(mock_state.dispatched), 1)
        action, payload = mock_state.dispatched[0]
        self.assertEqual(action, "set")
        self.assertEqual(payload["key"], "counter")
        self.assertEqual(payload["value"], "0")

if __name__ == '__main__':
    unittest.main()
