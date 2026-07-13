import unittest
from runtime.stdlib.modules.math_lib import MATH_MODULE
from runtime.stdlib.modules.string_lib import STRING_MODULE
from runtime.stdlib.modules.json_lib import JSON_MODULE
from runtime.stdlib.modules.file_lib import FILE_MODULE
from runtime.values.number import NumberValue
from runtime.values.string import StringValue
from runtime.values.map import MapValue
from runtime.values.list import ListValue

class TestStdlibAll(unittest.TestCase):
    def test_math(self):
        MATH_MODULE['pow'].function([NumberValue(2), NumberValue(3)])
        MATH_MODULE['sqrt'].function([NumberValue(16)])
        MATH_MODULE['round'].function([NumberValue(3.14)])
        MATH_MODULE['floor'].function([NumberValue(3.9)])
        MATH_MODULE['ceil'].function([NumberValue(3.1)])
        MATH_MODULE['abs'].function([NumberValue(-5)])
        MATH_MODULE['min'].function([NumberValue(1), NumberValue(2)])
        MATH_MODULE['max'].function([NumberValue(1), NumberValue(2)])
        MATH_MODULE['sin'].function([NumberValue(0)])
        MATH_MODULE['cos'].function([NumberValue(0)])
        MATH_MODULE['tan'].function([NumberValue(0)])

    def test_string(self):
        STRING_MODULE['upper'].function([StringValue("a")])
        STRING_MODULE['lower'].function([StringValue("A")])
        STRING_MODULE['replace'].function([StringValue("ab"), StringValue("b"), StringValue("c")])
        STRING_MODULE['contains'].function([StringValue("ab"), StringValue("b")])
        STRING_MODULE['split'].function([StringValue("a,b"), StringValue(",")])
        STRING_MODULE['trim'].function([StringValue(" a ")])
        STRING_MODULE['starts_with'].function([StringValue("ab"), StringValue("a")])
        STRING_MODULE['ends_with'].function([StringValue("ab"), StringValue("b")])

    def test_json(self):
        m = MapValue()
        m.set("a", NumberValue(1))
        JSON_MODULE['serialize'].function([m])
        JSON_MODULE['parse'].function([StringValue('{"a": 1}')])

    def test_file(self):
        import tempfile
        import os
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"hello")
            f.flush()
            FILE_MODULE['read_text'].function([StringValue(f.name)])
            FILE_MODULE['write_text'].function([StringValue(f.name), StringValue("world")])
            FILE_MODULE['exists'].function([StringValue(f.name)])
            FILE_MODULE['delete'].function([StringValue(f.name)])

if __name__ == '__main__':
    unittest.main()
