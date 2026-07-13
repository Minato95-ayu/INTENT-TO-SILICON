import unittest
from runtime.stdlib.registry import StdLibRegistry
from runtime.stdlib.modules.file_lib import register_file_lib
from runtime.stdlib.modules.json_lib import register_json_lib
from runtime.stdlib.modules.crypto_lib import register_crypto_lib
from runtime.stdlib.modules.database_lib import register_database_lib
from runtime.stdlib.modules.regex_lib import register_regex_lib
from runtime.values.string import StringValue
from runtime.memory.heap import Heap

class MockVM:
    def __init__(self):
        self.heap = Heap()

def create_string(vm, text):
    obj = vm.heap.allocate("string", text)
    return StringValue(obj.id, vm.heap)

class TestStdLibE2E(unittest.TestCase):
    def setUp(self):
        self.registry = StdLibRegistry()
        register_file_lib(self.registry)
        register_json_lib(self.registry)
        register_crypto_lib(self.registry)
        register_database_lib(self.registry)
        register_regex_lib(self.registry)
        self.vm = MockVM()

    def test_json_e2e(self):
        fn_parse = self.registry.functions.get("json::parse")
        res = fn_parse([create_string(self.vm, '{"hello": "world"}')], self.vm)
        
        # Searching the map elements for a string value matching "hello"
        found_val = res._get_payload().get("hello")
        self.assertEqual(found_val.to_python(), "world")

    def test_crypto_e2e(self):
        fn_sha = self.registry.functions.get("crypto::sha256")
        res = fn_sha([create_string(self.vm, "test")], self.vm)
        self.assertEqual(res.to_python(), "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08")

    def test_regex_e2e(self):
        fn_match = self.registry.functions.get("regex::match")
        res = fn_match([create_string(self.vm, "^[a-z]+$"), create_string(self.vm, "test")], self.vm)
        self.assertTrue(res.value)
        
    def test_database_e2e(self):
        fn_connect = self.registry.functions.get("db::connect")
        fn_query = self.registry.functions.get("db::query")
        
        cid = fn_connect([create_string(self.vm, ":memory:")], self.vm)
        self.assertIsNotNone(cid.to_python())
        
        # Test creation and insertion
        fn_query([cid, create_string(self.vm, "CREATE TABLE test (id INT, name TEXT)")], self.vm)
        fn_query([cid, create_string(self.vm, "INSERT INTO test VALUES (1, 'aayu')")], self.vm)
        
        res = fn_query([cid, create_string(self.vm, "SELECT name FROM test WHERE id=1")], self.vm)
        self.assertEqual(len(res._get_payload()), 1)
        
        row_map = res._get_payload()[0]
        found_val = row_map._get_payload().get("name")
        self.assertEqual(found_val.to_python(), "aayu")

if __name__ == '__main__':
    unittest.main()
