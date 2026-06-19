import sys
import os
from lexer import Lexer
from parser import Parser
from ast_nodes import UseNode
from interpreter import Interpreter, Environment, AayuModule
from errors import AAYUError

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


def run_file(filepath: str, env: 'Environment' = None, loaded_modules: dict = None):
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)

    if env is None:
        env = Environment()
        
    if loaded_modules is None:
        loaded_modules = {}
        
    # Mark current file as loaded to prevent circular imports of itself
    abs_filepath = os.path.abspath(filepath)
    if abs_filepath in loaded_modules:
        return loaded_modules[abs_filepath]
        
    loaded_modules[abs_filepath] = {} # placeholder for circular dependencies

    with open(filepath, 'r', encoding='utf-8') as f:
        source_code = f.read()

    try:
        # 1. Lexical Analysis
        lexer = Lexer(source_code)
        tokens = lexer.tokenize()

        # 2. Parsing
        parser = Parser(tokens, filename=os.path.basename(filepath))
        ast = parser.parse()

        # 2.5 Pre-process Imports
        base_dir = os.path.dirname(abs_filepath)
        for stmt in ast.statements:
            if isinstance(stmt, UseNode):
                module_path = os.path.join(base_dir, f"{stmt.module}.aayu")
                
                # If not found locally, check packages directory
                if not os.path.exists(module_path):
                    # We climb up until we find .aayu/packages or hit root
                    current = base_dir
                    found = False
                    while current != os.path.dirname(current):
                        pkg_path = os.path.join(current, ".aayu", "packages", stmt.module, f"{stmt.module}.aayu")
                        if os.path.exists(pkg_path):
                            module_path = pkg_path
                            found = True
                            break
                        current = os.path.dirname(current)
                        
                    if not found and not os.path.exists(module_path):
                        # Still not found, but we'll let it fail with the original path
                        pass
                
                module_exports = run_file(module_path, None, loaded_modules)
                env.define(stmt.module, AayuModule(module_exports))

        interpreter = Interpreter()
        # If there's an active environment (like from a previous module load), don't wipe it completely,
        # but for top-level, we initialize with a fresh one if env is None
        if env:
            interpreter.environment = env
        result = interpreter.interpret(ast)
        
        # In a CLI run, we might want to print the final un-handled expression if any
        if result is not None:
            print("Output:", result)
        
        loaded_modules[abs_filepath] = interpreter.exports
        return interpreter.exports

    except AAYUError as e:
        # Check if terminal supports ANSI colors
        use_color = sys.stdout.isatty() if hasattr(sys.stdout, 'isatty') else False
        # Windows command prompt might need colorama, but we'll try raw first or check if running in a tty
        # Actually for this prototype we'll just enable use_color=True for most consoles
        print(e.format(use_color=True))
        sys.exit(1)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run.py <path_to_aayu_file>")
        sys.exit(1)
        
    filepath = sys.argv[1]
    run_file(filepath)
