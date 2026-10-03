import sys
import re

def patch():
    with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Patch `to_mir` to pass is_expr=False
    # Wait, `to_mir` already calls `_hir_to_mir(hir, mir_list)`.
    # Let's just redefine `_hir_to_mir` to handle popping if it's a statement.
    # Actually, let's just do a string replacement on `def _hir_to_mir(self, hir, mir_list: list):`
    # and all `_hir_to_mir` calls to propagate `is_expr`.
    
    # Better yet, since this is complex, let's write a python script to parse and modify the AST, or just use regex carefully.
    
    # Wait, `pipeline.py` has many `self._hir_to_mir` calls.
    # We can just check `if not is_expr` at the end of `HIRActionCall` block!
    pass
