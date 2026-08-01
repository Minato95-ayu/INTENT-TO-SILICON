
import sys

try:
    import os
    from aayu.compiler.lexer.lexer import Lexer
    from aayu.compiler.parser.parser import Parser
    from aayu.compiler.ast.nodes import ImportNode, ProgramNode
    
    target = "stthomas_app/app.aayu"
    with open(target, "r", encoding="utf-8") as f:
        mod_source = f.read()
    lexer = Lexer(mod_source)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
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
                            m_src = mf.read()
                        m_ast = Parser(Lexer(m_src).tokenize()).parse()
                        m_ast = load_imports(m_ast, base_dir, visited)
                        new_statements.extend(m_ast.statements)
            else:
                new_statements.append(stmt)
        return ProgramNode(line=program_node.line, column=program_node.column, statements=new_statements)
        
    ast = load_imports(ast, os.path.dirname(os.path.abspath(target)), set([os.path.abspath(target)]))
    
    from aayu.compiler.semantic.analyzer import SemanticAnalyzer
    analyzer = SemanticAnalyzer()
    semantic_ast = analyzer.analyze(ast)
    
    from aayu.compiler.ir.pipeline import IRPipeline
    pipeline = IRPipeline()
    lir = pipeline.to_lir(pipeline.to_mir(pipeline.to_hir(semantic_ast)))
    
    from aayu.compiler.bytecode.encoder import BytecodeEncoder
    encoder = BytecodeEncoder()
    program = encoder.encode(lir)
    
    from aayu.runtime.vm.vm import VirtualMachine
    vm = VirtualMachine()
    vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)
    vm.execute()
    
    print("Before call_action: root=", vm.interpreter.render_tree.root)
    vm.call_action_by_name("__PAGE_START__")
    vm.execute()
    
    print("Tree root after execute:", vm.interpreter.render_tree.root)
    print("Node stack:", vm.interpreter.node_stack)
except Exception as e:
    import traceback
    traceback.print_exc()

