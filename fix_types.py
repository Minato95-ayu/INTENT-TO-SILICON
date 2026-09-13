with open('compiler/semantic/analyzer.py', 'r') as f:
    content = f.read()

replacement = """        sym_true = Symbol("true", "boolean")
        sym_true.is_constant = True
        sym_true.data_type = "Boolean"
        self.global_scope.define(sym_true)

        sym_false = Symbol("false", "boolean")
        sym_false.is_constant = True
        sym_false.data_type = "Boolean"
        self.global_scope.define(sym_false)

        sym_null = Symbol("null", "Null")
        sym_null.is_constant = True
        sym_null.data_type = "Null"
        self.global_scope.define(sym_null)"""

import re
content = re.sub(r'sym_true = Symbol\("true", "boolean"\).*?self\.global_scope\.define\(sym_null\)', replacement, content, flags=re.DOTALL)

with open('compiler/semantic/analyzer.py', 'w') as f:
    f.write(content)
