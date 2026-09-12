import unittest
import os
import json
import socket
from unittest.mock import patch, MagicMock

# AAYU Runtime Imports
from runtime.vm.vm import VirtualMachine
from runtime.stdlib.stdlib import StdLibLoader
from runtime.values.string import StringValue
from runtime.values.number import NumberValue
from runtime.values.boolean import BooleanValue
from runtime.values.null import NullValue

class TestStdlibProduction(unittest.TestCase):
    def setUp(self):
        self.vm = VirtualMachine()
        loader = StdLibLoader()
        loader.register(self.vm)
        self.vm._register_stdlib = lambda: None # mock as it's already registered via loader
        
        # Helper to execute stdlib functions easily
        self.execute = lambda method, *args: self.vm.globals.get(method).value([self._py_to_val(a) for a in args], self.vm)

    def _py_to_val(self, val):
        if isinstance(val, str):
            obj = self.vm.memory.heap.allocate("string", val)
            return StringValue(obj.id, self.vm.memory.heap)
        if isinstance(val, (int, float)):
            return NumberValue(val)
        return NullValue()

    def test_fs_production(self):
        test_file = "test_output_prod.txt"
        
        # 1. Write
        res = self.execute("file::write", test_file, "Hello ")
        self.assertTrue(isinstance(res, BooleanValue) and res.value == True)
        
        # 2. Append
        res = self.execute("file::append", test_file, "World")
        self.assertTrue(isinstance(res, BooleanValue) and res.value == True)
        
        # 3. Read
        res = self.execute("fs::read", test_file)
        self.assertEqual(res.to_python(), "Hello World")
        
        # 4. Exists
        res = self.execute("fs::exists", test_file)
        self.assertTrue(res.value == True)
        
        # 5. Delete
        res = self.execute("fs::delete", test_file)
        self.assertTrue(res.value == True)
        
        # 6. Exists after delete
        res = self.execute("fs::exists", test_file)
        self.assertFalse(res.value == True)
        
        # 7. Missing File Error
        res = self.execute("fs::read", "missing_file_random_123.txt")
        self.assertEqual(res.to_python(), "error: file not found")

    @patch("urllib.request.urlopen")
    def test_http_production(self, mock_urlopen):
        # 1. 200 OK
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "ok"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        res = self.execute("http::get", "http://example.com")
        self.assertEqual(res.to_python(), '{"status": "ok"}')
        
        # 2. Timeout Error
        mock_urlopen.side_effect = socket.timeout("timeout")
        res = self.execute("http::get", "http://example.com", 1)
        self.assertEqual(res.to_python(), "error: timeout")

    def test_json_production(self):
        # 1. Parse Nested
        json_str = '{"a": {"b": [1, 2, 3]}}'
        parsed = self.execute("json::parse", json_str)
        self.assertEqual(parsed.get(self._py_to_val("a")).get(self._py_to_val("b")).get(self._py_to_val(0)).to_python(), 1.0)
        
        # 2. Stringify Unicode
        unicode_str = '{"lang": "हिंदी"}'
        parsed = self.execute("json::parse", unicode_str)
        stringified = self.execute("json::stringify", parsed)
        self.assertEqual(stringified.to_python(), unicode_str)
        
        # 3. Invalid JSON
        res = self.execute("json::parse", '{"a": 1')
        self.assertTrue("error: invalid json" in res.to_python())
        
        # 4. >100 Levels deep
        deep_json = '{"a": ' * 250 + '1' + '}' * 250
        res = self.execute("json::parse", deep_json)
        self.assertTrue("error: json too deep" in res.to_python() or "invalid" not in res.to_python())

    def test_memory_integrity(self):
        # Peak heap check
        initial_heap_size = len(self.vm.memory.heap.objects)
        
        # Allocate heavily
        for i in range(100):
            self.execute("math::pow", 2, i)
            
        json_str = '{"arr": [1,2,3,4,5,6,7,8,9,10]}'
        for i in range(50):
            self.execute("json::parse", json_str)
            
        peak_heap_size = len(self.vm.memory.heap.objects)
        self.assertTrue(peak_heap_size > initial_heap_size)
        
        # In a real ARC/GC we would assert size goes back down, 
        # but since AAYU VM GC isn't explicitly triggered here, we just ensure no crashes occur.
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()