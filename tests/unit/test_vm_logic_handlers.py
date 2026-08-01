import unittest
from aayu.runtime.vm.handlers.logic import execute_and, execute_or, execute_not
from aayu.runtime.values.boolean import BooleanValue

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

class TestVMLogicHandlers(unittest.TestCase):
    def setUp(self):
        self.vm = DummyVM()
        self.frame = DummyFrame()

    def test_and(self):
        self.frame.stack.push(BooleanValue(True))
        self.frame.stack.push(BooleanValue(False))
        execute_and(self.vm, self.frame, 0)
        self.assertFalse(self.frame.stack.pop().value)

    def test_or(self):
        self.frame.stack.push(BooleanValue(True))
        self.frame.stack.push(BooleanValue(False))
        execute_or(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

    def test_not(self):
        self.frame.stack.push(BooleanValue(False))
        execute_not(self.vm, self.frame, 0)
        self.assertTrue(self.frame.stack.pop().value)

if __name__ == '__main__':
    unittest.main()
