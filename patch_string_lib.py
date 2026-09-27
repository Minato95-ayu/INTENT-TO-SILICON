with open("runtime/stdlib/modules/string_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

new_functions = """
def fn_substring(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    start = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    end = int(args[2].to_python()) if not isinstance(args[2], (int, float)) else int(args[2])
    return StringValue(s[start:end])

def fn_char_at(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return StringValue("")
    return StringValue(s[index])

def fn_char_code(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return NumberValue(-1)
    return NumberValue(ord(s[index]))
"""

if "def fn_substring" not in content:
    content = content.replace("def register_string_lib(registry: StdLibRegistry):", new_functions + "\ndef register_string_lib(registry: StdLibRegistry):")

regs = """    registry.register("string::substring", fn_substring)
    registry.register("string::char_at", fn_char_at)
    registry.register("string::char_code", fn_char_code)
"""

if "string::substring" not in content:
    content = content.replace('registry.register("string::length", fn_length)', 'registry.register("string::length", fn_length)\n' + regs)

with open("runtime/stdlib/modules/string_lib.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated string_lib.py")
