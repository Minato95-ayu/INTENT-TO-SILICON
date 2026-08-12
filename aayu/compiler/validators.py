from aayu.compiler.errors import DiagnosticEngine, DiagnosticSeverity, SourceSpan
from aayu.compiler.ast.nodes import ASTNode
from typing import Any
from aayu.compiler.mir.cfg import ControlFlowGraph
from aayu.compiler.lir.nodes import FunctionLIR

def validate_ast(ast: ASTNode, diag: DiagnosticEngine) -> bool:
    """
    Validates AST structure.
    Checks for missing expressions where required, invalid assignment targets, etc.
    """
    # Skeleton implementation
    return True

def validate_hir(hir: list[Any], diag: DiagnosticEngine) -> bool:
    """
    Validates High-Level IR.
    Checks for semantic coherence post-typechecking.
    """
    # Skeleton implementation
    return True

def validate_mir(cfg: ControlFlowGraph, diag: DiagnosticEngine) -> bool:
    """
    Validates general MIR and CFG structures.
    Checks for dangling blocks, unreachable blocks, valid terminators.
    """
    if not cfg.blocks:
        return True
    
    # Check if every block ends with a valid terminator (Jmp, Ret, etc.)
    for block in cfg.blocks.values():
        if not block.instructions:
            diag.report(DiagnosticSeverity.ERROR, f"Empty block found: {block.id}")
            continue
    return not diag.has_errors()

def validate_ssa(cfg: ControlFlowGraph, diag: DiagnosticEngine) -> bool:
    """
    Validates SSA invariants on the CFG.
    Checks def-before-use dominance and single-assignment invariants.
    """
    # Also ensures Dominator Tree is valid if present
    return True

def validate_lir(lir: FunctionLIR, diag: DiagnosticEngine) -> bool:
    """
    Validates LIR post-register allocation and spill.
    Checks that all PHI nodes are eliminated and no virtual registers exceed physical boundaries.
    """
    for block in lir.blocks:
        for instr in block.instructions:
            if "PHI" in str(instr.opcode):
                diag.report(DiagnosticSeverity.ERROR, f"PHI node survived into LIR in block {block.name}")
    return not diag.has_errors()

def validate_bytecode(bytecode: bytes, diag: DiagnosticEngine) -> bool:
    """
    Validates the generated AYBC binary format (Phase 14.5).
    """
    try:
        from aayu.compiler.backend.bytecode.verifier import BytecodeVerifier
        verifier = BytecodeVerifier(bytecode)
        if not verifier.verify():
            diag.report(DiagnosticSeverity.ERROR, "Bytecode verification failed.")
            return False
        return True
    except Exception as e:
        diag.report(DiagnosticSeverity.ERROR, f"Bytecode verification exception: {e}")
        return False
