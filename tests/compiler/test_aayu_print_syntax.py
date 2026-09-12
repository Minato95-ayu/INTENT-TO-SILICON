from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser


def test_aayu_native_print_syntax_parses_without_parentheses():
    ast = Parser(Lexer('print "Hello AAYU".').tokenize()).parse()

    statement = ast.statements[0]
    assert type(statement).__name__ == "ActionCallNode"
    assert statement.name == "print"
    assert statement.args[0].value == "Hello AAYU"


def test_legacy_print_call_syntax_remains_supported():
    ast = Parser(Lexer('print("Hello AAYU").').tokenize()).parse()

    statement = ast.statements[0]
    assert statement.name == "print"
    assert statement.args[0].value == "Hello AAYU"