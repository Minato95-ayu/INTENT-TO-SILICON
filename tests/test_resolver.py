import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from aayu.compiler.resolver import MiniLexer

def test_mini_lexer():
    source = """
    // This is a comment import foo
    import auth
    
    state welcome_msg = "Hello import db"
    
    /* 
       import models
       Multi-line comment
    */
    
    import database.mysql
    import ui
    
    action test() {
        print("don't import me")
    }
    """
    
    lexer = MiniLexer(source)
    imports = lexer.extract_imports()
    
    assert "auth" in imports, "Failed to parse standard import"
    assert "database.mysql" in imports, "Failed to parse nested import"
    assert "ui" in imports, "Failed to parse import"
    
    assert "foo" not in imports, "Parsed import inside single-line comment"
    assert "db" not in imports, "Parsed import inside string literal"
    assert "models" not in imports, "Parsed import inside multi-line comment"
    assert "me" not in imports, "Parsed import inside string literal"
    
    print(f"[OK] MiniLexer extracted imports correctly! Found: {imports}")

if __name__ == "__main__":
    test_mini_lexer()
