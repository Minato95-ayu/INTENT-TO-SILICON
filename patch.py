with open("compiler/semantic/analyzer.py", "r") as f:
    code = f.read()
code = code.replace("self._enter_scope()", "prev = self.current_scope\n            self.current_scope = SymbolTable(parent=prev)")
code = code.replace("self._exit_scope()", "self.current_scope = prev")
with open("compiler/semantic/analyzer.py", "w") as f:
    f.write(code)
