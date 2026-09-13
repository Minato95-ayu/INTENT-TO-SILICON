import re
with open('compiler/semantic/analyzer.py', 'r') as f:
    content = f.read()

replacement = """        # Inject true, false, null constants
        sym_true = Symbol("true", "boolean")
        sym_true.is_constant = True
        sym_true.data_type = "Boolean"
        self.global_scope.define(sym_true)"""

content = re.sub(r'# Inject true, false, null constants\s*sym_true = Symbol\("true", "boolean"\)\s*sym_true\.is_constant = True\s*sym_true\.data_type = "Boolean"\s*self\.global_scope\.define\(sym_true\)', replacement, content)

with open('compiler/semantic/analyzer.py', 'w') as f:
    f.write(content)
