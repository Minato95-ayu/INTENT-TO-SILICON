import unittest
from aayu.runtime.vm.handlers.math import execute_add, execute_sub, execute_mul, execute_div, execute_eq, execute_neq, execute_lt, execute_gt, execute_lte, execute_gte
from aayu.runtime.values.number import NumberValue

class DummyStack:
    def __init__(self):
        self.items = []
    def push(self, val):
        self.items.append(val)
    def pop(self):
        return self.items.pop()

class DummyFrame:
    def __init__(self):
        self.stack = DummyStack()
        self.ip = 0

class DummyVM:
    pass

class TestVMMathHandlers(unittest.TestCase):
    def setUp(self):
        self.vm = DummyVM()
        self.frame = DummyFrame()

    def test_add(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_add(self.vm, self.frame, 0)
        self.assertEqual(self.frame.stack.pop().value, 8)

    def test_sub(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_sub(self.vm, self.frame, 0)
        self.assertEqual(self.frame.stack.pop().value, 2)
        
    def test_mul(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_mul(self.vm, self.frame, 0)
        self.assertEqual(self.frame.stack.pop().value, 15)
        
    def test_div(self):
        self.frame.stack.push(NumberValue(6))
        self.frame.stack.push(NumberValue(2))
        execute_div(self.vm, self.frame, 0)
        self.assertEqual(self.frame.stack.pop().value, 3)

    def test_eq(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(5))
        execute_eq(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_neq(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_neq(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_lt(self):
        self.frame.stack.push(NumberValue(3))
        self.frame.stack.push(NumberValue(5))
        execute_lt(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_gt(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_gt(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_lte(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(5))
        execute_lte(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_gte(self):
        self.frame.stack.push(NumberValue(5))
        self.frame.stack.push(NumberValue(3))
        execute_gte(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

if __name__ == '__main__':
    unittest.main()
