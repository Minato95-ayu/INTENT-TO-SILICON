from aayu_language.lexer import Lexer
from aayu_language.parser import Parser
from aayu_language.interpreter import Interpreter
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

# Mock DB
class MockCursor:
    def execute(self, *args):
        pass
    def fetchall(self):
        # return two rows
        return [{'id': 1, 'title': 'A'}, {'id': 2, 'title': 'B'}]

interpreter.db_cursor = MockCursor()

# Define Book entity so find works
interpreter.evaluate(ast.statements[0])

# Execute task api_books
task_node = ast.statements[1]
interpreter.environment.define("api_books", task_node)
interpreter.environment.define("req", {"path": "/api/books"})

try:
    interpreter.evaluate(task_node.body[0]) # list books is find Book.
    print("Environment books:", interpreter.environment.get("books"))
    
    ret = interpreter.evaluate(task_node.body[1]) # return json books.
    print("Return:", ret)
except Exception as e:
    import traceback
    traceback.print_exc()
