import os

vm_path = r"prototype\language\runtime\vm\vm.py"
with open(vm_path, "r", encoding="utf-8") as f:
    vm_content = f.read()

vm_content = vm_content.replace("from ..values.null import NullValue\n", "")
vm_content = "from ..values.null import NullValue\nfrom ..values.number import NumberValue\nfrom ..values.string import StringValue\nfrom ..values.boolean import BooleanValue\nfrom ..values.function import FunctionValue, NativeFunctionValue\nfrom ..values.list import ListValue\nfrom ..values.map import MapValue\n" + vm_content

with open(vm_path, "w", encoding="utf-8") as f:
    f.write(vm_content)
    
print("Fixed vm.py imports")
