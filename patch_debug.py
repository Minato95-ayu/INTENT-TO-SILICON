with open("runtime/stdlib/helpers.py", "r", encoding="utf-8") as f:
    content = f.read()

if "print(" not in content:
    content = content.replace('def make_string(vm, text: str) -> StringValue:\n    obj_id = vm.heap.allocate("string", text)', 'def make_string(vm, text: str) -> StringValue:\n    obj_id = vm.heap.allocate("string", text)\n    print(f"Allocated obj_id={obj_id} for text={repr(text)} in heap {id(vm.heap)}")')
    with open("runtime/stdlib/helpers.py", "w", encoding="utf-8") as f:
        f.write(content)

with open("runtime/values/string.py", "r", encoding="utf-8") as f:
    content = f.read()

if "print(" not in content:
    content = content.replace("    def _get_payload(self) -> str:\n        return self.heap.read(self.heap_id)['value']", "    def _get_payload(self) -> str:\n        print(f'Reading obj_id={self.heap_id} from heap {id(self.heap)}')\n        obj = self.heap.read(self.heap_id)\n        if obj is None:\n            print('OBJ IS NONE!')\n            print(self.heap.allocator.pool.pool.keys())\n        return obj['value']")
    with open("runtime/values/string.py", "w", encoding="utf-8") as f:
        f.write(content)
