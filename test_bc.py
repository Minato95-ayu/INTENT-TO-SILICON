import io
import contextlib
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler

code = """
        project MassiveTest.
    
        storage TestDB.
    
        model User {
            id Int.
            name String.
            is_active Boolean.
        }
    
        task main.
            let x: Int = 10.
            let y: Int = 20.
            let z: Int = math::max(x, y).
    
            let name: String = "AAYU".
            let numbers: List = [1, 2, 3].
            let info: Map = {"key": "value"}.
    
            if x > 5.
                core::print("Greater").
            end.
    
            if x < 15.
                core::print("Less").
            else.
                core::print("No").
            end.
    
            let i: Int = 0.
            while x < 0.
                let i: Int = math::max(i, 1).
            end.
    
            for each n in numbers.
                core::print(n).
            end.
    
    
            try.
                throw "Error".
            catch (e).
                core::print(e).
            finally.
                core::print("Done").
            end.
    
            function helper(a: Int): Int
                return math::max(a, 1).
            end.
    
            let h: Int = helper(5).
    
            insert User {
                id = 1.
                name = "Test".
                is_active = true.
            }
    
            let u: List = find User.
            update User {
                name = "Updated".
            }
            delete User.
        end.
    
        run main.
"""

lexer = Lexer(code)
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()
compiler = AAYUCompiler()
bytecode = compiler.compile(ast)

def print_bytecode(bc, indent=""):
    for i, inst in enumerate(bc.instructions):
        print(f"{indent}{i:4d}: {inst.opcode.name} {inst.operand if inst.operand is not None else ''}")

print("MAIN:")
print_bytecode(bytecode)

if bytecode.constants:
    print("CONSTANTS:")
    for i, c in enumerate(bytecode.constants):
        if hasattr(c, 'instructions'):
            print(f"  Const {i} (Function/Task):")
            print_bytecode(c, "    ")
        else:
            print(f"  Const {i}: {c}")

