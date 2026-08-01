import unittest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.compiler.passes.manager import PassManager
from aayu.runtime.vm.vm import VirtualMachine
import io
import contextlib

class TestMassiveSyntax(unittest.TestCase):
    def test_massive_syntax(self):
        source = """
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
            while false.
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
        
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        parser = Parser(tokens, filename="<test>")
        ast = parser.parse()
        
        compiler = BytecodeEncoder(filename="<test>")
        bytecode = compiler.compile(ast)
        
        vm = VirtualMachine()
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            vm.run(bytecode)
            
        output = f.getvalue()
        self.assertIn("Greater", output)
        self.assertIn("Error", output)
        self.assertIn("Done", output)

if __name__ == '__main__':
    unittest.main()
