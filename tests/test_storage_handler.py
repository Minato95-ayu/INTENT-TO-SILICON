import unittest
from aayu.compiler.lexer.lexer import Lexer
from aayu.compiler.parser.parser import Parser
from aayu.compiler.bytecode.encoder import BytecodeEncoder
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.manager import RuntimeManager
from aayu.runtime.database.runtime import DatabaseRuntime
import os

@unittest.skip(
    "Legacy syntax: 'insert'/'find' keywords removed from parser. "
    "Re-enable after db::insert/db::find stdlib methods are implemented. "
    "See: NoneType crash hypothesis — parked, investigate during E2E."
)
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
        app TestApp
        
        model TestUser {
            id: Int
            name: String
        }
        
        action main
            insert TestUser {
                name = "AAYU_User"
            }
            
            users = find TestUser
            return users
        end
        run main
        """
        lexer = Lexer(code)
        parser = Parser(lexer.tokenize())
        ast = parser.parse()
        
        compiler = BytecodeEncoder()
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
