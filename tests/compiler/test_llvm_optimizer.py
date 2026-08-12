import pytest
pytest.importorskip("llvmlite")

from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMBasicBlock
from aayu.compiler.backend.llvm.types import i32
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.bridge import LLVMBridge

def test_llvm_bridge_optimizer():
    module = LLVMModule("test_opt")
    func = LLVMFunction("main", i32)
    module.add_function(func)
    
    block = LLVMBasicBlock("entry", func)
    func.blocks.append(block)
    
    builder = IRBuilder()
    builder.position_at_end(block)
    
    from aayu.compiler.backend.llvm.values import LLVMConstantInt
    a = LLVMConstantInt(i32, 10)
    b = LLVMConstantInt(i32, 20)
    
    # Dead code, should be optimized away
    res = builder.add(a, b)
    
    val = LLVMConstantInt(i32, 42)
    builder.ret(val)
    
    bridge = LLVMBridge()
    ll_mod = bridge.parse_module(module)
    
    # Before optimization
    ir_before = str(ll_mod)
    assert "add i32 10, 20" in ir_before
    
    # Optimize
    bridge.optimize(ll_mod, profile="ReleaseFast")
    
    # After optimization
    ir_after = str(ll_mod)
    # LLVM's instruction combining/DCE should remove the unused add
    assert "add" not in ir_after
