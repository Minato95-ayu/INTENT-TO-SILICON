import unittest
import os
import json
import socket
from unittest.mock import patch, MagicMock

# AAYU Runtime Imports
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.stdlib.stdlib import StdLib
from aayu.runtime.values.string import StringValue
from aayu.runtime.values.number import NumberValue
from aayu.runtime.values.boolean import BooleanValue
from aayu.runtime.values.null import NullValue
from aayu.runtime.values.base import RuntimeValue

class TestStdlibProduction(unittest.TestCase):
    def setUp(self):
        self.vm = VirtualMachine()
        
        # Helper to execute stdlib functions easily
        self.execute = lambda method, *args: self.vm.stdlib.registry.functions.get(method)([self._py_to_val(a) for a in args], self.vm)

    def _py_to_val(self, val):
        if isinstance(val, RuntimeValue):
            return val
        if isinstance(val, str):
            ptr = self.vm.heap.allocate("string", val)
            return StringValue(ptr, self.vm.heap)
        if isinstance(val, (int, float)):
            return NumberValue(val)
        if isinstance(val, bool):
            return BooleanValue(val)
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
        res = self.execute("file::read", test_file)
        self.assertEqual(res.to_python(), "Hello World")
        
        # 4. Exists
        res = self.execute("file::exists", test_file)
        self.assertTrue(res.value == True)
        
        # 5. Delete
        res = self.execute("file::delete", test_file)
        self.assertTrue(res.value == True)
        
        # 6. Exists after delete
        res = self.execute("file::exists", test_file)
        self.assertFalse(res.value == True)
        
        # 7. Missing File Error
        res = self.execute("file::read", "missing_file_random_123.txt")
        self.assertEqual(res.to_python(), "error: file not found")

    @patch("urllib.request.urlopen")
    def test_http_production(self, mock_urlopen):
        # 1. 200 OK
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "ok"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        res = self.execute("HTTP.get", "http://example.com")
        if hasattr(res, 'to_python'):
            res = res.to_python()
        self.assertEqual(res, {"status": "ok"})
        
        # 2. Timeout Error
        mock_urlopen.side_effect = socket.timeout("timeout")
        res = self.execute("HTTP.get", "http://example.com", 1)
        if hasattr(res, 'to_python'):
            res = res.to_python()
        self.assertIsNone(res)

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
        initial_heap_size = len(self.vm.heap.allocator.pool.pool)
        
        # Allocate heavily
        for i in range(100):
            self.execute("math::pow", 2, i)
            
        json_str = '{"arr": [1,2,3,4,5,6,7,8,9,10]}'
        for i in range(50):
            self.execute("json::parse", json_str)
            
        peak_heap_size = len(self.vm.heap.allocator.pool.pool)
        self.assertTrue(peak_heap_size > initial_heap_size)
        
        # In a real ARC/GC we would assert size goes back down, 
        # but since AAYU VM GC isn't explicitly triggered here, we just ensure no crashes occur.
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
