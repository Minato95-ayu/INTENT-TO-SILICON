
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/semantic/errors.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

new_code = """
class TypeError(Exception):
    def __init__(self, expected: str, received: str, line: int, column: int, hint: str = ""):
        message = f"\\nType Error\\n"
        message += f"Line {line}, Column {column}\\n"
        message += f"Expected: {expected}\\n"
        message += f"Received: {received}\\n"
        if hint:
            message += f"Hint: {hint}\\n"
            
        super().__init__(message)
        self.line = line
        self.column = column
        self.expected = expected
        self.received = received
        self.hint = hint
"""
if "class TypeError" not in c:
    c += new_code
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print("Patched errors.py")

