import pytest
import sys
import os

# Add root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from compiler.lexer.lexer import Lexer
from compiler.parser.parser import Parser
from compiler.errors import CompilerError

def test_compiler_error_formatting():
    err = CompilerError("Expected string after title", line=4, column=15, source_line='title button')
    formatted = str(err)
    assert "Expected string after title (Line 4, Col 15)" in formatted
    assert "title button" in formatted
    assert "              ^" in formatted

def test_parser_recovery_and_errors():
    sources = [
        "page Home\ntitle button\nend",
        "state count = \npage Home\nend",
        "invalid_keyword count = 10",
        "state @count = 10",
        "page Home\n  child {\nend",
        "page Home\n  child 123\nend",
        "page Home" # Missing end
    ]
    
    # We will just verify that for 1000 random invalid tokens, the compiler raises CompilerError instead of crashing with a traceback.
    import random
    keywords = ["page", "state", "end", "title", "button"]
    symbols = ["=", "@", "#", "{", "}"]
    
    for i in range(1000):
        # Generate garbage
        garbage = " ".join(random.choices(keywords + symbols + ["123", "abc", '""'], k=10))
        
        lexer = Lexer(garbage)
        try:
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            parser.parse()
        except CompilerError as e:
            # Expected behavior
            assert e.line > 0
        except Exception as e:
            pytest.fail(f"Compiler crashed on garbage input: {garbage}. Exception: {e}")

if __name__ == '__main__':
    pytest.main(['-v', __file__])
