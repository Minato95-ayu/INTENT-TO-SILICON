
with open("runtime/stdlib/modules/ai_lib.py", "r", encoding="utf-8") as f:
    code = f.read()
code = code.replace("args[0].to_python()", "(_value(args[0]))")
code = code.replace("args[1].to_python()", "(_value(args[1]))")
code = "def _value(val):\n    return val.to_python() if hasattr(val, \"to_python\") else val\n" + code

with open("runtime/stdlib/modules/ai_lib.py", "w", encoding="utf-8") as f:
    f.write(code)

