# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import unittest
import os
import json
import socket
from unittest.mock import patch, MagicMock

# AAYU Runtime Imports
from runtime.vm.vm import VirtualMachine
from runtime.stdlib.stdlib import StdLib
from runtime.values.base import RuntimeValue
from runtime.values.string import StringValue
from runtime.values.number import NumberValue
from runtime.values.boolean import BooleanValue
from runtime.values.null import NullValue

class TestStdlibProduction(unittest.TestCase):
    def setUp(self):
        self.vm = VirtualMachine()
        loader = StdLib(self.vm)
        self.loader = loader
        # Helper to execute stdlib functions easily
        self.execute = lambda method, *args: self.loader.registry.call(method, [self._py_to_val(a) for a in args], self.vm)

    def _py_to_val(self, val):
        if isinstance(val, RuntimeValue):
            return val
        if isinstance(val, str):
            obj = self.vm.heap.allocate("string", val)
            return StringValue(obj, self.vm.heap)
        if isinstance(val, (int, float)):
            return NumberValue(float(val))
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
        
        # 4. Delete
        res = self.execute("file::delete", test_file)
        self.assertTrue(isinstance(res, BooleanValue) and res.value == True)
        
        # 5. Missing File
        with self.assertRaises(Exception) as context:
            self.execute("file::read", test_file)
        self.assertIn("file not found", str(context.exception))

    @patch("urllib.request.urlopen")
    def test_http_production(self, mock_urlopen):
        # 1. 200 OK
        mock_response = MagicMock()
        mock_response.read.return_value = b'{"status": "ok"}'
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        res = self.execute("HTTP.get", "http://example.com")
        self.assertEqual(res, {"status": "ok"})
        
        # 2. 404 Not Found
        mock_response.getcode.return_value = 404
        mock_response.read.return_value = b'Not Found'
        mock_urlopen.return_value = mock_response
        
        res = self.execute("HTTP.get", "http://example.com/missing")
        self.assertEqual(res, "Not Found")

    def test_json_production(self):
        # 1. Parse Nested
        json_str = '{"a": {"b": [1, 2, 3]}}'
        parsed = self.execute("json::parse", json_str)
        val = parsed.get(self._py_to_val("a")).get(self._py_to_val("b")).get(self._py_to_val(0)).to_python()
        self.assertEqual(val, 1.0)
        
        # 2. Stringify Unicode
        unicode_str = '{"lang": "\u0939\u093f\u0902\u0926\u0940"}'
        parsed = self.execute("json::parse", unicode_str)
        stringified = self.execute("json::stringify", parsed)
        self.assertEqual(stringified.to_python(), unicode_str)
        
        # 3. Invalid JSON
        res = self.execute("json::parse", '{"a": 1')
        self.assertTrue("error" in str(res.to_python()).lower())

    def test_memory_integrity(self):
        # Peak heap check
        initial_heap_size = len(self.vm.heap.allocator.pool.pool)
        
        # Allocate heavily
        for i in range(100):
            self.execute("math::pow", 2, i)
            
        json_str = '{"arr": [1,2,3,4,5,6,7,8,9,10]}'
        for i in range(50):
            self.execute("json::parse", json_str)
            
        final_heap_size = len(self.vm.heap.allocator.pool.pool)
        self.assertTrue(final_heap_size > initial_heap_size)

if __name__ == '__main__':
    unittest.main()


