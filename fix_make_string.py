with open("runtime/stdlib/modules/string_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

old_func = """def fn_substring(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    start = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    end = int(args[2].to_python()) if not isinstance(args[2], (int, float)) else int(args[2])
    return StringValue(s[start:end], heap=vm.heap)

def fn_char_at(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return StringValue("", heap=vm.heap)
    return StringValue(s[index], heap=vm.heap)

def fn_char_code(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return NumberValue(-1, heap=vm.heap)
    return NumberValue(ord(s[index]), heap=vm.heap)"""

new_func = """def fn_substring(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    start = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    end = int(args[2].to_python()) if not isinstance(args[2], (int, float)) else int(args[2])
    return make_string(vm, s[start:end])

def fn_char_at(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return make_string(vm, "")
    return make_string(vm, s[index])

def fn_char_code(args, vm):
    s = args[0].to_python() if not isinstance(args[0], str) else args[0]
    index = int(args[1].to_python()) if not isinstance(args[1], (int, float)) else int(args[1])
    if index < 0 or index >= len(s):
        return -1
    return ord(s[index])"""

if old_func in content:
    content = content.replace(old_func, new_func)
    with open("runtime/stdlib/modules/string_lib.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed string_lib.py to use make_string")
else:
    print("Code not found in string_lib.py")
