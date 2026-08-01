
with open("tools/commands/run.py", "r") as f:
    code = f.read()

import_logic = """
        ast = parser.parse()
        
        # --- MODULE LOADER PASS ---
        import os
        from aayu.compiler.ast.nodes import ImportNode, ProgramNode
        from aayu.compiler.lexer.lexer import Lexer as ModLexer
        from aayu.compiler.parser.parser import Parser as ModParser
        
        def load_imports(program_node, base_dir, visited):
            new_statements = []
            for stmt in program_node.statements:
                if isinstance(stmt, ImportNode):
                    mod_path = stmt.module.replace(".", "/") + ".aayu"
                    full_path = os.path.join(base_dir, mod_path)
                    
                    if full_path not in visited:
                        visited.add(full_path)
                        if os.path.exists(full_path):
                            with open(full_path, "r", encoding="utf-8") as mf:
                                mod_source = mf.read()
                            mod_ast = ModParser(ModLexer(mod_source).tokenize()).parse()
                            mod_ast = load_imports(mod_ast, base_dir, visited)
                            new_statements.extend(mod_ast.statements)
                        else:
                            print(f"Error: Module {stmt.module} not found at {full_path}")
                            sys.exit(1)
                else:
                    new_statements.append(stmt)
            return ProgramNode(line=program_node.line, column=program_node.column, statements=new_statements)
            
        base_directory = os.path.dirname(os.path.abspath(target))
        if not base_directory:
            base_directory = "."
            
        ast = load_imports(ast, base_directory, set([os.path.abspath(target)]))
        # --- END MODULE LOADER ---
"""

code = code.replace("ast = parser.parse()", import_logic)

with open("tools/commands/run.py", "w") as f:
    f.write(code)

