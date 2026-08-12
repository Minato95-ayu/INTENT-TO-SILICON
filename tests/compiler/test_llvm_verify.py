import pytest
pytest.importorskip("llvmlite")

from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMBasicBlock
from aayu.compiler.backend.llvm.types import i32
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.bridge import LLVMBridge

def test_llvm_bridge_verify_success():
    module = LLVMModule("test_verify")
    func = LLVMFunction("main", i32)
    module.add_function(func)
    
    block = LLVMBasicBlock("entry", func)
    func.blocks.append(block)
    
    builder = IRBuilder()
    builder.position_at_end(block)
    
    from aayu.compiler.backend.llvm.values import LLVMConstantInt
    val = LLVMConstantInt(i32, 42)
    builder.ret(val)
    
    bridge = LLVMBridge()
    ll_mod = bridge.parse_module(module)
    
    # Verify should succeed without exceptions
    assert bridge.verify(ll_mod) is True
