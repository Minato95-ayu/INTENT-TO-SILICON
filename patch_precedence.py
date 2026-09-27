with open("runtime/stdlib/modules/file_lib.py", "r", encoding="utf-8") as f:
    text = f.read()

text = text.replace(
    'if len(args) > 1 and args[1] if isinstance(args[1], str) else args[1].to_python() == "binary":',
    'if len(args) > 1 and (args[1] if isinstance(args[1], str) else args[1].to_python()) == "binary":'
)

with open("runtime/stdlib/modules/file_lib.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Fixed precedence in file_lib.py")
