with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    text = f.read()

# First revert my incorrect hack in _semantic_to_hir
target1 = """        elif isinstance(node, SemanticTryNode):
            try_hir = []
            for s in node.try_block:
                h = self._semantic_to_hir(s)
                if h is not None:
                    try_hir.append(h)
                    if self._needs_pop(h): try_hir.append(HIRPop())
            catch_hir = []
            for s in node.catch_block:
                h = self._semantic_to_hir(s)
                if h is not None:
                    catch_hir.append(h)
                    if self._needs_pop(h): catch_hir.append(HIRPop())
            finally_hir = []
            for s in node.finally_block:
                h = self._semantic_to_hir(s)
                if h is not None:
                    finally_hir.append(h)
                    if self._needs_pop(h): finally_hir.append(HIRPop())
            return HIRTry(try_hir, node.catch_var, catch_hir, finally_hir)"""

replacement1 = """        elif isinstance(node, SemanticTryNode):
            try_hir = [self._semantic_to_hir(s) for s in node.try_block if self._semantic_to_hir(s) is not None]
            catch_hir = [self._semantic_to_hir(s) for s in node.catch_block if self._semantic_to_hir(s) is not None]
            finally_hir = [self._semantic_to_hir(s) for s in node.finally_block if self._semantic_to_hir(s) is not None]
            return HIRTry(try_hir, node.catch_var, catch_hir, finally_hir)"""

text = text.replace(target1, replacement1)

# Now fix the missing pop in _hir_to_mir
target2 = """            mir_list.append(MIRInstruction("SETUP_EXCEPT", [error_target]))
            for stmt in hir.try_block:
                self._hir_to_mir(stmt, mir_list)
            mir_list.append(MIRInstruction("POP_EXCEPT", []))
            mir_list.append(MIRInstruction("JUMP", [finally_label]))
            if hir.catch_block:
                mir_list.append(MIRInstruction("LABEL", [catch_label]))
                if hir.catch_var:
                    # Exception object is on stack
                    mir_list.append(MIRInstruction("SET_STATE", [hir.catch_var]))
                else:
                    # discard exception if not captured
                    mir_list.append(MIRInstruction("POP", []))
                    
                for stmt in hir.catch_block:
                    self._hir_to_mir(stmt, mir_list)
                
                mir_list.append(MIRInstruction("JUMP", [finally_label]))
            mir_list.append(MIRInstruction("LABEL", [finally_label]))
            for stmt in hir.finally_block:
                self._hir_to_mir(stmt, mir_list)"""

replacement2 = """            mir_list.append(MIRInstruction("SETUP_EXCEPT", [error_target]))
            for stmt in hir.try_block:
                self._hir_to_mir(stmt, mir_list)
                if self._needs_pop(stmt): mir_list.append(MIRInstruction("POP", []))
            mir_list.append(MIRInstruction("POP_EXCEPT", []))
            mir_list.append(MIRInstruction("JUMP", [finally_label]))
            if hir.catch_block:
                mir_list.append(MIRInstruction("LABEL", [catch_label]))
                if hir.catch_var:
                    # Exception object is on stack
                    mir_list.append(MIRInstruction("SET_STATE", [hir.catch_var]))
                else:
                    # discard exception if not captured
                    mir_list.append(MIRInstruction("POP", []))
                    
                for stmt in hir.catch_block:
                    self._hir_to_mir(stmt, mir_list)
                    if self._needs_pop(stmt): mir_list.append(MIRInstruction("POP", []))
                
                mir_list.append(MIRInstruction("JUMP", [finally_label]))
            mir_list.append(MIRInstruction("LABEL", [finally_label]))
            for stmt in hir.finally_block:
                self._hir_to_mir(stmt, mir_list)
                if self._needs_pop(stmt): mir_list.append(MIRInstruction("POP", []))"""

text = text.replace(target2, replacement2)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed POP in try blocks")
