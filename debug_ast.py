from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
code = """
action test()
    return 42
    print(999)
end
"""
lexer = Lexer(code)
ast = Parser(lexer.tokenize()).parse()
action_node = ast.statements[0]
print(vars(action_node))
