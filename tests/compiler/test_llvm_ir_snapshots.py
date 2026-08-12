import pytest
from aayu.compiler.backend.llvm.values import (
    LLVMModule, LLVMFunction, LLVMBasicBlock, LLVMConstantInt
)
from aayu.compiler.backend.llvm.types import i32
from aayu.compiler.backend.llvm.builder import IRBuilder
from aayu.compiler.backend.llvm.serializer import LLVMSerializer
from aayu.compiler.backend.llvm.verifier import LLVMIRVerifier
from aayu.compiler.errors import DiagnosticEngine

def test_llvm_ir_snapshot():
    # 1. Build a simple LLVM IR graph using the fluent builder
    module = LLVMModule("test_module")
    
    # define i32 @add(i32 %a, i32 %b)
    func = LLVMFunction("add_nums", i32)
    module.add_function(func)
    
    # args
    from aayu.compiler.backend.llvm.values import LLVMArgument
    arg_a = LLVMArgument(i32, "a", func)
    arg_b = LLVMArgument(i32, "b", func)
    func.args = [arg_a, arg_b]
    
    block = LLVMBasicBlock("entry", func)
    func.blocks.append(block)
    
    builder = IRBuilder()
    builder.position_at_end(block)
    
    # %v0 = add i32 %a, %b
    res = builder.add(arg_a, arg_b)
    
    # ret i32 %v0
    builder.ret(res)
    
    # 2. Verify
    diag = DiagnosticEngine()
    verifier = LLVMIRVerifier(diag)
    assert verifier.verify(module) is True
    assert not diag.has_errors()
    
    # 3. Serialize
    serializer = LLVMSerializer()
    ll_string = serializer.serialize(module)
    
    # 4. Snapshot check
    expected = (
        "; ModuleID = 'test_module'\n"
        "source_filename = \"test_module\"\n\n"
        "define i32 @add_nums(i32 %a, i32 %b) {\n"
        "entry:\n"
        "  %v0 = add i32 %a, %b\n"
        "  ret i32 %v0\n"
        "}\n"
    )
    
    assert ll_string == expected

def test_llvm_ir_verifier_type_mismatch():
    module = LLVMModule("test_fail")
    func = LLVMFunction("fail", i32)
    module.add_function(func)
    
    block = LLVMBasicBlock("entry", func)
    func.blocks.append(block)
    
    builder = IRBuilder()
    builder.position_at_end(block)
    
    from aayu.compiler.backend.llvm.types import i64
    a = LLVMConstantInt(i32, 10)
    b = LLVMConstantInt(i64, 20) # Mismatch
    
    builder.add(a, b)
    builder.ret(a)
    
    diag = DiagnosticEngine()
    verifier = LLVMIRVerifier(diag)
    assert verifier.verify(module) is False
    assert len(diag.diagnostics) > 0
    assert "Type mismatch in add: i32 vs i64" in diag.diagnostics[0].message
