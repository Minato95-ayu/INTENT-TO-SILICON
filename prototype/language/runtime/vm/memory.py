class Memory:
    def __init__(self):
        self.globals = {}
        self.constants = []
        self.heap = {}  # Future support for Objects, Arrays, Maps, Strings
