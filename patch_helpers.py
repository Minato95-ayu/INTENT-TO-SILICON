with open("runtime/stdlib/helpers.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace('def make_string(vm, text: str) -> StringValue:\n    obj_id = vm.heap.allocate("string", text)', 'def make_string(vm, text: str) -> StringValue:\n    obj_id = vm.heap.allocate("string", text)\n    #print(f"Allocated {obj_id} for {repr(text)}")')

with open("runtime/stdlib/helpers.py", "w", encoding="utf-8") as f:
    f.write(content)
