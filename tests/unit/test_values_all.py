import unittest
from aayu.runtime.values.string import StringValue
from aayu.runtime.values.list import ListValue
from aayu.runtime.values.map import MapValue
from aayu.runtime.values.number import NumberValue

class TestValuesAll(unittest.TestCase):
    def test_string(self):
        s = StringValue("hello")
        self.assertEqual(s.value, "hello")
        self.assertEqual(str(s), "hello")
        
        # Test methods
        # methods are added by stdlib, but we can test basic ones if any exist
        # We also want to test equality and hashing
        s2 = StringValue("hello")
        s3 = StringValue("world")
        self.assertEqual(s, s2)
        self.assertNotEqual(s, s3)
        self.assertEqual(hash(s), hash(s2))
        
        # Try some string ops
        s4 = s + s3
        self.assertEqual(s4.value, "helloworld")

    def test_list(self):
        l = ListValue([NumberValue(1), NumberValue(2)])
        self.assertEqual(len(l.elements), 2)
        self.assertEqual(str(l), "[1, 2]")
        
        l.elements.append(NumberValue(3))
        self.assertEqual(len(l.elements), 3)
        
        l2 = ListValue([NumberValue(1), NumberValue(2), NumberValue(3)])
        self.assertEqual(l, l2)

    def test_map(self):
        m = MapValue()
        m.set("a", NumberValue(1))
        self.assertEqual(m.get("a").value, 1)
        self.assertEqual(str(m), '{"a": 1}')
        
        m2 = MapValue()
        m2.set("a", NumberValue(1))
        self.assertEqual(m, m2)

if __name__ == '__main__':
    unittest.main()
