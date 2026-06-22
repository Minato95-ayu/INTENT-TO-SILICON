import os
import sys
import json

def run_explain(filepath: str):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        return
        
    try:
        cli_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.append(os.path.join(cli_dir, "aayu_language"))
        sys.path.append(cli_dir)

        from aayu_language.lexer import Lexer
        from aayu_language.parser import Parser
        from aayu_language.ir_generator import generate_ir
        
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        ir_json_str = generate_ir(ast)
        ir_data = json.loads(ir_json_str)
        
        system_name = ir_data.get("system", {}).get("name", "Unknown System")
        entities = [e.get("name") for e in ir_data.get("entities", [])]
        pages = [p.get("name") for p in ir_data.get("pages", [])]
        workflows = [w.get("name") for w in ir_data.get("workflows", [])]
        
        print(f"System: {system_name}\n")
        
        print("Entities:")
        if entities:
            for e in entities:
                print(f"- {e}")
        else:
            print("- None")
            
        print("\nPages:")
        if pages:
            for p in pages:
                print(f"- {p}")
        else:
            print("- None")
            
        print("\nWorkflows:")
        if workflows:
            for w in workflows:
                print(f"- {w}")
        else:
            print("- None")
            
    except Exception as e:
        print(f"Error parsing file: {e}")
