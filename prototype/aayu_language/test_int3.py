from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, ReturnException
import json

code = """
entity Book.
    text title.
end.

task api_books with req.
    list books is find Book.
    return json books.
end.
"""

lexer = Lexer(code)
parser = Parser(lexer.tokenize())
ast = parser.parse()

interpreter = Interpreter()

class MockCursor:
    def execute(self, *args):
        pass
    def fetchall(self):
        return [{'id': 1, 'title': 'A'}, {'id': 2, 'title': 'B'}]

interpreter.db_cursor = MockCursor()
interpreter.evaluate(ast.statements[0])

task_node = ast.statements[1]
interpreter.environment.define("api_books", task_node)
interpreter.environment.define("req", {"path": "/api/books"})

try:
    interpreter.evaluate(task_node.body[0]) # list books is find Book.
    
    interpreter.evaluate(task_node.body[1]) # return json books.
except ReturnException as e:
    ret = e.value
    print("Return data_str:", ret.data_str)
except Exception as e:
    import traceback
    traceback.print_exc()
