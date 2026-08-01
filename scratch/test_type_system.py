
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.semantic.analyzer import SemanticAnalyzer
from aayu.compiler.semantic.type_inference import TypeInference
from aayu.compiler.semantic.type_checker import TypeChecker
from aayu.compiler.semantic.errors import TypeError

def check_code(code: str):
    print(f"\n--- Checking Code ---\n{code}")
    lexer = Lexer(code)
    parser = Parser(lexer.tokenize())
    ast = parser.parse()
    
    analyzer = SemanticAnalyzer()
    semantic_ast = analyzer.analyze(ast)
    
    infer = TypeInference()
    semantic_ast = infer.infer(semantic_ast)
    
    checker = TypeChecker()
    checker.check(semantic_ast)
    print("Pass!")

def test_type_system():
    # 1. Valid Assignment
    valid_code = """
    app TypeTest
    page Home
        state age = 20
        action inc
            age = 21
        end
    end
    """
    check_code(valid_code)
    
    # 2. Invalid Assignment (Negative Test)
    invalid_code = """
    app TypeTest
    page Home
        state age = 20
        action inc
            age = "twenty one"
        end
    end
    """
    try:
        check_code(invalid_code)
        print("FAIL: Expected TypeError for invalid assignment")
    except TypeError as e:
        print("Caught expected TypeError:")
        print(e)
        
    # 3. Invalid Binary Op
    invalid_bin_op = """
    app TypeTest
    page Home
        state name = "Ayush"
        action do
            state result = name - 5
        end
    end
    """
    try:
        check_code(invalid_bin_op)
        print("FAIL: Expected TypeError for invalid binary op")
    except TypeError as e:
        print("Caught expected TypeError:")
        print(e)
        
    # 4. Valid List
    valid_list = """
    app TypeTest
    page Home
        state numbers = [1, 2, 3]
    end
    """
    check_code(valid_list)
        
if __name__ == "__main__":
    test_type_system()

