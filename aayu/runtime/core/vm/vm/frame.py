class CallFrame:
    """Represents a single function call frame."""
    def __init__(self, function_name: str, return_ip: int, locals_count: int = 0):
        self.function_name = function_name
        self.return_ip = return_ip
        self.locals = [None] * locals_count
