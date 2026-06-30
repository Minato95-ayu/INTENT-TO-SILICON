class Stack:
    def __init__(self):
        self._stack = []

    def push(self, value):
        self._stack.append(value)

    def pop(self):
        if not self._stack:
            raise IndexError("pop from empty stack")
        return self._stack.pop()
        
    def peek(self):
        if not self._stack:
            raise IndexError("peek from empty stack")
        return self._stack[-1]
        
    def is_empty(self):
        return len(self._stack) == 0

    def __len__(self):
        return len(self._stack)
