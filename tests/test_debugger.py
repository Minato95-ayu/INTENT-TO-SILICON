import pytest
import threading
import time
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.vm.config import VMConfig
from aayu.runtime.vm.instructions import Opcode
from aayu.runtime.debugger.session import DebugSession

class MockProtocol:
    def __init__(self):
        self.responses = []
        
    def send_response(self, req, body=None):
        self.responses.append((req, body))
        
    def send_event(self, event, body=None):
        pass

class MockSession(DebugSession):
    def __init__(self, debugger):
        self.debugger = debugger
        self.protocol = MockProtocol()
        
def test_debugger_breakpoints():
    vm = VirtualMachine(VMConfig.development())
    
    # Tiny mock bytecode:
    # 0: PUSH 10
    # 3: HALT
    bytecode = bytearray()
    bytecode.append(Opcode.PUSH_CONST)
    bytecode.extend((0).to_bytes(2, 'little'))
    bytecode.append(Opcode.HALT)
    
    vm.load(bytecode, constant_pool=[10])
    
    # Load debug symbols
    vm.debugger.load_debug_symbols({
        "map": {
            0: {"line": 1, "file": "main.aayu"},
            3: {"line": 2, "file": "main.aayu"}
        }
    })
    
    # Set breakpoint at line 2 (IP 3)
    vm.debugger.breakpoints.set_breakpoint(2)
    
    # Run VM in background thread
    vm_thread = threading.Thread(target=vm.interpreter.run)
    vm_thread.start()
    
    # Wait for breakpoint hit
    time.sleep(0.1)
    
    # Ensure VM is paused and snapshot is taken
    assert vm.debugger.is_paused is True
    assert vm.debugger.snapshot is not None
    assert vm.debugger.snapshot.ip == 3
    
    # Test session response
    session = MockSession(vm.debugger)
    
    # Fetch stack trace
    req = {"command": "stackTrace", "seq": 1}
    session.handle_request(req)
    
    # Stack frames should be returned
    assert len(session.protocol.responses) == 1
    resp = session.protocol.responses[0]
    assert resp[0]["command"] == "stackTrace"
    
    # Continue
    req = {"command": "continue", "seq": 2}
    session.handle_request(req)
    
    # VM should finish
    vm_thread.join(timeout=1.0)
    assert not vm_thread.is_alive()
    assert vm.registers.ip == 3 # HALT doesn't increment IP

if __name__ == '__main__':
    pytest.main(['-v', __file__])
