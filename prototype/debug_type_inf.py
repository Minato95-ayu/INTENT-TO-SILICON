import sys
sys.path.insert(0, 'd:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language')
from lexer import Lexer
from parser import Parser
from passes.semantic.scope_builder import ScopeBuilderPass
from passes.semantic.type_checker import TypeCheckerPass
from compiler_context import CompilerContext
from resolver.symbols import SymbolTable, ScopeType

c = CompilerContext()
c.current_module = 'test'
c.symbol_tables['test'] = SymbolTable('test', ScopeType.GLOBAL)
source = 'let x is 5. x is "hello".'
l = Lexer(source)
p = Parser(l.tokenize(), 'test.aayu')
ast = p.parse()
c.ast = ast
c.asts['test'] = ast
ScopeBuilderPass().run(c)
TypeCheckerPass().run(c)
print('Errors:', c.diagnostics.diagnostics)
assign_node = ast.statements[1]
print('Target resolved type:', assign_node.target.resolved_type)
print('Target symbol:', assign_node.target.symbol)
if assign_node.target.symbol:
    print('Target symbol resolved type:', assign_node.target.symbol.resolved_type)
print('Value resolved type:', assign_node.value.resolved_type)
