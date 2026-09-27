with open("runtime/stdlib/modules/string_lib.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("return StringValue(s[start:end])", "return StringValue(s[start:end], heap=vm.heap)")
content = content.replace('return StringValue("")', 'return StringValue("", heap=vm.heap)')
content = content.replace("return StringValue(s[index])", "return StringValue(s[index], heap=vm.heap)")
content = content.replace("return NumberValue(-1)", "return NumberValue(-1, heap=vm.heap)")
content = content.replace("return NumberValue(ord(s[index]))", "return NumberValue(ord(s[index]), heap=vm.heap)")

with open("runtime/stdlib/modules/string_lib.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Fixed heap references in string_lib.py")
