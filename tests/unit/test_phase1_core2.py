import pytest
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from compiler.frontend.ast_nodes import *
from compiler.frontend.errors import AAYUSyntaxError

def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def compile_source(source):
    ast = parse(source)
    compiler = AAYUCompiler()
    return compiler.compile(ast)

class TestParserAdvanced:
    def test_module_import_export(self):
        ast = parse('''
        module MyModule.
        import std.math as m.
        export task my_task() { return 1. }
        public task p_task() { return 2. }
        private let hidden = 3.
        ''')
        assert len(ast.statements) == 5

    def test_list_and_map_declaration(self):
        ast = parse('''
        list my_list.
        map my_map.
        list config is [1, 2].
        map user is { "name": "ayush" }.
        ''')
        assert len(ast.statements) == 4

    def test_record_declaration(self):
        ast = parse('''
        record Point.
            x: int
            y: int
        end.
        ''')
        assert len(ast.statements) == 1
        
    def test_operators(self):
        ast = parse('''
        let a = 1 + 2 * 3 / 4 - 5.
        let b = (a == 5) and (a != 6) or (a > 2).
        let c = not true.
        let d = -a.
        ''')
        assert len(ast.statements) == 4
        
    def test_property_access(self):
        ast = parse('''
        let val = x of obj.
        ''')
        assert len(ast.statements) == 1
        
    def test_set_and_add(self):
        ast = parse('''
        add "item" to my_list.
        set "name" to "Ayush" in my_map.
        ''')
        assert len(ast.statements) == 2

    def test_v1_1_unsupported(self):
        with pytest.raises(AAYUSyntaxError):
            parse('page Home.')

class TestCompilerAdvanced:
    def test_compile_operators(self):
        bytecode = compile_source('''
        let a = 1 + 2 * 3 / 4 - 5.
        let b = (a == 5) and (a != 6) or (a > 2).
        let c = not true.
        let d = -a.
        ''')
        assert bytecode
        
    def test_compile_module(self):
        bytecode = compile_source('''
        module MathLib.
        export task square(x) {
            return x * x.
        }
        ''')
        assert bytecode

    def test_compile_lists_maps_mutations(self):
        bytecode = compile_source('''
        list my_list.
        map my_map.
        add 1 to my_list.
        set "age" to 25 in my_map.
        ''')
        assert bytecode
