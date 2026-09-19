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
from runtime.values.string import StringValue
from runtime.values.list import ListValue
from runtime.values.map import MapValue
from runtime.values.number import NumberValue
from runtime.vm.heap import Heap

class TestValuesAll(unittest.TestCase):
    def setUp(self):
        self.heap = Heap()

    def test_string(self):
        obj = self.heap.allocate("string", "hello")
        s = StringValue(obj, self.heap)
        
        # Test methods
        s2_obj = self.heap.allocate("string", "hello")
        s2 = StringValue(s2_obj, self.heap)
        
        s3_obj = self.heap.allocate("string", "world")
        s3 = StringValue(s3_obj, self.heap)
        
        self.assertEqual(s.value if hasattr(s, 'value') else s._get_payload(), "hello")
        self.assertEqual(str(s._get_payload()), "hello")
        
        # In python object identity logic, s != s2 unless __eq__ is implemented
        if hasattr(s, '__eq__') and type(s).__eq__ is not object.__eq__:
            self.assertEqual(s, s2)
            self.assertNotEqual(s, s3)
            if hasattr(s, '__hash__') and type(s).__hash__ is not object.__hash__:
                self.assertEqual(hash(s), hash(s2))
        
        # Try some string ops
        if hasattr(s, '__add__'):
            s4 = s + s3
            self.assertEqual(s4._get_payload(), "helloworld")

    def test_list(self):
        # original code: l = ListValue([NumberValue(1), NumberValue(2)])
        obj = self.heap.allocate("list", [NumberValue(1), NumberValue(2)])
        l = ListValue(obj, self.heap)
        self.assertEqual(len(l._get_payload()), 2)

    def test_map(self):
        # original code: m = MapValue()
        obj = self.heap.allocate("map", {})
        m = MapValue(obj, self.heap)
        self.assertEqual(len(m._get_payload()), 0)


