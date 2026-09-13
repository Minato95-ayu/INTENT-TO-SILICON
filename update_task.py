content = """
## R4.3: Pipeline Rewiring (Out-of-SSA / Linearizer)
- [x] Create `Linearizer` pass for Out-of-SSA conversion
- [x] Implement PHI elimination via pseudo `COPY` mapping
- [x] Serialize CFG blocks into flat instruction list with `LABEL`s
- [x] Map Virtual Registers (SSA `Value`s) to VM stack local variables (e.g., `"%vX"`)
- [x] Lower 3AC operations to target Stack Bytecode semantics (`PUSH_CONST`, `BINARY_+`, `LOAD_VAR`, `STORE_VAR`)
- [x] E2E Integration: End-to-end VM execution using `test_r4_3_backend.py` (Math and Branching executes natively)
- [x] Unit Tests: Formal invariant checks for `test_phi_elimination_and_linearization`, `test_block_serialization`
"""
with open(r'C:\Users\Miinato\.gemini\antigravity\brain\3563ad77-9877-42ad-8cb3-ab3799b3a56b\task.md', 'a') as f:
    f.write(content)
