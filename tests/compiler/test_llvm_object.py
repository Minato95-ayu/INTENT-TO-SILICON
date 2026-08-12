import pytest
pytest.importorskip("llvmlite")

from aayu.compiler.backend.llvm.values import LLVMModule, LLVMFunction, LLVMBasicBlock
from aayu.compiler.backend.llvm.types import i32
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.bridge import LLVMBridge

def test_llvm_bridge_emit_object():
    module = LLVMModule("test_obj")
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
    bridge.verify(ll_mod)
    
    # Emit object
    obj_bytes = bridge.emit_object(ll_mod)
    assert len(obj_bytes) > 0
    assert obj_bytes.startswith(b'\x7fELF') or obj_bytes.startswith(b'\xfe\xed\xfa\xce') or obj_bytes.startswith(b'\xcf\xfa\xed\xfe') or obj_bytes.startswith(b'L\x01') or obj_bytes.startswith(b'd\x86') # ELF or Mach-O or COFF
    
    # Emit assembly
    asm_str = bridge.emit_assembly(ll_mod)
    assert len(asm_str) > 0
    assert "main" in asm_str
