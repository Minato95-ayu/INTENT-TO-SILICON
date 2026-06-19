import os
import sys
import unittest
import sqlite3
import io
import contextlib

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "aayu_language"))

from lexer import Lexer
from parser import Parser
from compiler import AAYUCompiler
from vm import VirtualMachine
from serializer import serialize, deserialize

class TestVMDatabase(unittest.TestCase):
    def setUp(self):
        self.tests_dir = os.path.dirname(__file__)
        self.db_path = os.path.join(self.tests_dir, "..", "aayu_db.sqlite")
        # Ensure fresh DB for reproducible runs
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        # Clean up database after run
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_vm_database_and_schema(self):
        """Compile and execute vm_db.aayu. Verify schema and table data in SQLite."""
        filepath = os.path.join(self.tests_dir, "vm_db.aayu")
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        
        vm = VirtualMachine()
        f_out = io.StringIO()
        with contextlib.redirect_stdout(f_out):
            vm.run(bytecode)
        
        # Verify output from VM
        output = f_out.getvalue().strip()
        self.assertIn("Ayush", output)
        
        # Verify SQLite schema tracking table _aayu_schema
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM _aayu_schema WHERE entity_name = 'User'")
        schema_rows = [dict(r) for r in cursor.fetchall()]
        
        self.assertEqual(len(schema_rows), 1)
        self.assertEqual(schema_rows[0]['field_name'], 'name')
        self.assertEqual(schema_rows[0]['field_type'], 'text')
        
        # Verify data inserted into User table
        cursor.execute("SELECT * FROM User")
        user_rows = [dict(r) for r in cursor.fetchall()]
        self.assertEqual(len(user_rows), 1)
        self.assertEqual(user_rows[0]['name'], 'Ayush')
        conn.close()
        vm.close()

    def test_vm_database_update(self):
        """Compile and execute vm_db_update.aayu. Verify record update on VM."""
        filepath = os.path.join(self.tests_dir, "vm_db_update.aayu")
        with open(filepath, 'r', encoding='utf-8') as f:
            source = f.read()
            
        lexer = Lexer(source)
        parser = Parser(lexer.tokenize(), filename=filepath)
        ast = parser.parse()
        
        compiler = AAYUCompiler()
        bytecode = compiler.compile(ast)
        
        # Verify serialization and deserialization
        serialized = serialize(bytecode)
        deserialized = deserialize(serialized)
        
        vm = VirtualMachine()
        f_out = io.StringIO()
        with contextlib.redirect_stdout(f_out):
            vm.run(deserialized)
            
        output = f_out.getvalue().strip()
        self.assertIn("Minato", output)
        self.assertNotIn("Ayush", output)  # Ayush should have been updated to Minato

        # Double check in SQLite
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User")
        rows = [dict(r) for r in cursor.fetchall()]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['name'], 'Minato')
        conn.close()
        vm.close()

    def test_json_and_rendering(self):
        """Verify standard library json_serialize and render_template function execution on VM."""
        vm = VirtualMachine()
        
        # Test render_template with a temp template file
        temp_tpl = os.path.join(self.tests_dir, "temp_tpl.html")
        with open(temp_tpl, 'w', encoding='utf-8') as f:
            f.write("Hello {{ name }}, you are {{ age }}!")
            
        try:
            rendered = vm.stdlib.render_template(temp_tpl, {"name": "Ayush", "age": 20})
            self.assertEqual(rendered, "Hello Ayush, you are 20!")
            
            # Test serialization
            resp = vm.stdlib.json_serialize({"key": "value"})
            self.assertEqual(resp.data_str, '{"key": "value"}')
        finally:
            if os.path.exists(temp_tpl):
                os.remove(temp_tpl)
            vm.close()

if __name__ == "__main__":
    unittest.main()
