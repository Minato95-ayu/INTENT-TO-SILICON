import pytest
pytest.importorskip("llvmlite")

from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMBasicBlock
from aayu.compiler.backend.llvm.types import i32
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.bridge import LLVMBridge

def test_llvm_bridge_jit_execution():
    module = LLVMModule("test_jit")
    func = LLVMFunction("jit_add", i32)
    module.add_function(func)
    
    # We want a function that just returns a constant 42 for now,
    # as LLVMBinaryOp with arguments is harder to call simply via ctypes void()->int
    block = LLVMBasicBlock("entry", func)
    func.blocks.append(block)
    
    builder = IRBuilder()
    builder.position_at_end(block)
    
    from aayu.compiler.backend.llvm.values import LLVMConstantInt
    a = LLVMConstantInt(i32, 20)
    b = LLVMConstantInt(i32, 22)
    
    res = builder.add(a, b)
    builder.ret(res)
    
    bridge = LLVMBridge()
    ll_mod = bridge.parse_module(module)
    bridge.verify(ll_mod)
    bridge.optimize(ll_mod)
    
    bridge.create_jit(ll_mod)
    result = bridge.run_function("jit_add")
    
    assert result == 42
