with open('compiler/semantic/analyzer.py', 'r') as f:
    content = f.read()

replacement = """sym.signature_args = arity
            self.global_scope.define(sym)

        # Inject true, false, null constants
        sym_true = Symbol("true", "boolean")
        sym_true.is_constant = True
        self.global_scope.define(sym_true)

        sym_false = Symbol("false", "boolean")
        sym_false.is_constant = True
        self.global_scope.define(sym_false)

        sym_null = Symbol("null", "Null")
        sym_null.is_constant = True
        self.global_scope.define(sym_null)"""

content = content.replace("sym.signature_args = arity\n            self.global_scope.define(sym)", replacement)

with open('compiler/semantic/analyzer.py', 'w') as f:
    f.write(content)
