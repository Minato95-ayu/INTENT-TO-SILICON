import pytest
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from compiler.frontend.ast_nodes import *

def parse(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()

def compile_source(source):
    ast = parse(source)
    compiler = AAYUCompiler()
    return compiler.compile(ast)

class TestParserDatabase:
    def test_entity_declaration(self):
        ast = parse('''
        entity User.
            text name.
            number age.
        end.
        ''')
        assert len(ast.statements) == 1
        assert isinstance(ast.statements[0], EntityDeclarationNode)

    def test_create_entity(self):
        ast = parse('''
        create User with my_map.
        ''')
        assert len(ast.statements) == 1

    def test_auth(self):
        ast = parse('''
        create account with my_map.
        login my_creds.
        logout my_req.
        guard session.
        ''')
        assert len(ast.statements) == 4

    def test_insert_entity(self):
        ast = parse('''
        insert User {
            name = "Ayush".
        }
        ''')
        assert len(ast.statements) == 1

    def test_update_entity(self):
        ast = parse('''
        update User {
            age = 26.
        }
        ''')
        assert len(ast.statements) == 1

    def test_delete_entity(self):
        ast = parse('''
        delete User.
        ''')
        assert len(ast.statements) == 1

class TestCompilerDatabase:
    def test_compile_entity_operations(self):
        bytecode = compile_source('''
        entity User.
            text name.
            number age.
        end.
        create User with my_map.
        insert User {
            name = "Ayush".
        }
        update User {
            age = 26.
        }
        delete User.
        create account with my_map.
        login my_creds.
        logout my_req.
        guard session.
        ''')
        assert bytecode
