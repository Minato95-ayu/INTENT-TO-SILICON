import unittest
from compiler.frontend.lexer import Lexer
from compiler.frontend.parser import Parser
from compiler.frontend.compiler import AAYUCompiler
from runtime.vm.vm import VirtualMachine
from runtime.manager import RuntimeManager
from runtime.database.runtime import DatabaseRuntime
import os

class TestStorageHandler(unittest.TestCase):
    def setUp(self):
        # Create a fresh database for testing
        if os.path.exists("aayu_data/Main.db"):
            os.remove("aayu_data/Main.db")
            
    def tearDown(self):
        try:
            if os.path.exists("aayu_data/Main.db"):
                os.remove("aayu_data/Main.db")
        except PermissionError:
            pass

    def test_database_insert_find(self):
        code = """
        project TestApp.
        storage Main.
        
        model TestUser {
            id Int.
            name String.
        }
        
        task main.
            insert TestUser {
                name = "AAYU_User".
            }
            
            let users is find TestUser.
            return users.
        end.
        run main.
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        
        data_ir = {
            "storages": [{"name": "Main", "type": "sqlite"}],
            "models": [{"name": "TestUser", "fields": [{"name": "id", "type": "Int"}, {"name": "name", "type": "String"}]}]
        }
        runtime_manager = RuntimeManager({"data_ir": data_ir})
        runtime_manager.initialize()
        
        vm = VirtualMachine(bytecode, runtime_manager)
        result = vm.run()
        
        print(f"DEBUG RESULT: {result}")
        print(f"DEBUG TYPE: {result.type_name}")
        self.assertIsNotNone(result)
        
        py_list = result.to_python()
        self.assertEqual(len(py_list), 1)
        self.assertEqual(py_list[0]["name"], "AAYU_User")

if __name__ == '__main__':
    unittest.main()
