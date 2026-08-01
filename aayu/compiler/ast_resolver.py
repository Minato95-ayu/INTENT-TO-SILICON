def resolve_ast_imports(node, base_dir, visited):
    from aayu.compiler.ast.nodes import ImportNode, ProgramNode, WidgetNode
    from aayu.compiler.lexer.lexer import Lexer
    from aayu.compiler.parser.parser import Parser
    from dataclasses import replace
    import os
    import sys

    if hasattr(node, 'statements') and isinstance(node.statements, list):
        new_stmts = []
        for stmt in node.statements:
            if isinstance(stmt, ImportNode):
                mod_path = stmt.module.replace(".", "/") + ".aayu"
                full_path = os.path.join(base_dir, mod_path)
                
                if full_path not in visited:
                    visited.add(full_path)
                    if os.path.exists(full_path):
                        with open(full_path, "r", encoding="utf-8") as mf:
                            mod_source = mf.read()
                        mod_ast = Parser(Lexer(mod_source).tokenize()).parse()
                        mod_ast = resolve_ast_imports(mod_ast, base_dir, visited)
                        new_stmts.extend(mod_ast.statements)
                    else:
                        print(f"Error: Module {stmt.module} not found at {full_path}")
                        sys.exit(1)
            else:
                new_stmts.append(resolve_ast_imports(stmt, base_dir, visited))
        node = replace(node, statements=new_stmts)

    if isinstance(node, WidgetNode):
        new_children = []
        for child in node.children:
            if isinstance(child, ImportNode):
                mod_path = child.module.replace(".", "/") + ".aayu"
                full_path = os.path.join(base_dir, mod_path)
                
                if full_path not in visited:
                    visited.add(full_path)
                    if os.path.exists(full_path):
                        with open(full_path, "r", encoding="utf-8") as mf:
                            mod_source = mf.read()
                        mod_ast = Parser(Lexer(mod_source).tokenize()).parse()
                        mod_ast = resolve_ast_imports(mod_ast, base_dir, visited)
                        new_children.extend(mod_ast.statements)
                    else:
                        print(f"Error: Module {child.module} not found at {full_path}")
                        sys.exit(1)
            else:
                new_children.append(resolve_ast_imports(child, base_dir, visited))
        node = replace(node, children=new_children)
        
    return node
