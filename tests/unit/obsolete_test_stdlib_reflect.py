import unittest
from runtime.stdlib.reflect_lib import _reflect_type_of, _reflect_methods, _reflect_has_method
from runtime.values.number import NumberValue
from runtime.values.string import StringValue

class TestStdlibReflect(unittest.TestCase):
    def test_reflect_type_of(self):
        val = _reflect_type_of([NumberValue(10)])
        self.assertEqual(val.value, "Int")
        val = _reflect_type_of([NumberValue(10.5)])
        self.assertEqual(val.value, "Float")
        val = _reflect_type_of([StringValue("test")])
        self.assertEqual(val.value, "String")
        val = _reflect_type_of([])
        self.assertEqual(val.value, "Null")

    def test_reflect_methods(self):
        val = _reflect_methods([StringValue("test")])
        self.assertIn(StringValue("upper"), val.elements)
        val = _reflect_methods([])
        self.assertEqual(len(val.elements), 0)

    def test_reflect_has_method(self):
        from runtime.values.boolean import BooleanValue
        val = _reflect_has_method([StringValue("test"), StringValue("upper")])
        self.assertEqual(val.value, True)
        val = _reflect_has_method([StringValue("test"), StringValue("not_exist")])
        self.assertEqual(val.value, False)
        val = _reflect_has_method([])
        self.assertEqual(val.value, False)

if __name__ == '__main__':
    unittest.main()
