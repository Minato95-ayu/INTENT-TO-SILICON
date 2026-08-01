
from aayu.runtime.renderers.web_renderer import serialize_node
import sys, os
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.ast.nodes import ImportNode, ProgramNode
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.ir.pipeline import IRPipeline
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine

target = "stthomas_app/app.aayu"
with open(target, "r", encoding="utf-8") as f:
    source = f.read()

ast = Parser(Lexer(source).tokenize()).parse()

def load_imports(program_node, base_dir, visited):
    new_statements = []
    for stmt in program_node.statements:
        if isinstance(stmt, ImportNode):
            mod_path = stmt.module.replace(".", "/") + ".aayu"
            full_path = os.path.join(base_dir, mod_path)
            if full_path not in visited:
                visited.add(full_path)
                with open(full_path, "r", encoding="utf-8") as mf:
                    mod_source = mf.read()
                m_ast = Parser(Lexer(mod_source).tokenize()).parse()
                m_ast = load_imports(m_ast, base_dir, visited)
                new_statements.extend(m_ast.statements)
        else:
            new_statements.append(stmt)
    return ProgramNode(line=program_node.line, column=program_node.column, statements=new_statements)

ast = load_imports(ast, os.path.dirname(os.path.abspath(target)), set([os.path.abspath(target)]))
semantic = SemanticAnalyzer().analyze(ast)
ir_pipeline = IRPipeline()
lir = ir_pipeline.to_lir(ir_pipeline.to_mir(ir_pipeline.to_hir(semantic)))
program = BytecodeEncoder().encode(lir)

vm = VirtualMachine()
vm.load(program.bytecode, list(program.constant_pool.values()), program.action_addresses)
vm.execute()

tree = vm.interpreter.render_tree
style_sheet = set()
serialized = serialize_node(tree.root, style_sheet)
import json
print(json.dumps(serialized, indent=2))

