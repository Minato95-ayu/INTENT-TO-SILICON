
with open("compiler/parser/parser.py", "r") as f:
    code = f.read()

code = code.replace(
    "if method_type not in [\"get\", \"post\"]:",
    "if method_type not in [\"get\", \"post\", \"delete\", \"update\", \"put\"]:"
)
code = code.replace(
    "Error: Expect 'get' or 'post' inside route, got",
    "Error: Expect HTTP method inside route, got"
)

with open("compiler/parser/parser.py", "w") as f:
    f.write(code)

