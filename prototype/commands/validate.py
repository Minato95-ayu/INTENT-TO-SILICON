import os
import sys

def run_validate(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
        
    try:
        cli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(cli_dir, "aayu_language"))
        sys.path.append(cli_dir)

        from aayu_language.lexer import Lexer
        from aayu_language.parser import Parser
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        entities = sum(1 for node in ast.statements if node.__class__.__name__ == "EntityDeclarationNode")
        pages = sum(1 for node in ast.statements if node.__class__.__name__ == "UIPageNode")
        workflows = sum(1 for node in ast.statements if node.__class__.__name__ == "WorkflowDefNode")
        
        print(f"\u2713 Syntax Valid ({filepath})")
        print(f"\u2713 Entities Found: {entities}")
        print(f"\u2713 Pages Found: {pages}")
        print(f"\u2713 Workflows Found: {workflows}")
        
    except Exception as e:
        if hasattr(e, "format"):
            print(e.format(use_color=True))
        else:
            print(f"Error parsing file: {e}")
