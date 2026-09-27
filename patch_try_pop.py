with open("compiler/ir/pipeline.py", "r", encoding="utf-8") as f:
    text = f.read()

target = """        elif isinstance(node, SemanticTryNode):
            try_hir = [self._semantic_to_hir(s) for s in node.try_block if self._semantic_to_hir(s) is not None]
            catch_hir = [self._semantic_to_hir(s) for s in node.catch_block if self._semantic_to_hir(s) is not None]
            finally_hir = [self._semantic_to_hir(s) for s in node.finally_block if self._semantic_to_hir(s) is not None]
            return HIRTry(try_hir, node.catch_var, catch_hir, finally_hir)"""

replacement = """        elif isinstance(node, SemanticTryNode):
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

text = text.replace(target, replacement)

with open("compiler/ir/pipeline.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed TryCatch Pop!")
