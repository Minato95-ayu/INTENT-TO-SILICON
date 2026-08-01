with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to import RenderTree and RenderNode
import_stmt = '''from aayu.runtime.vm.instructions import Opcode
from aayu.runtime.vm.exceptions import KernelError
from aayu.runtime.vm.result import ResultStatus
import time
from aayu.runtime.ui.render_tree import RenderTree, RenderNode'''

content = content.replace(
'''from aayu.runtime.vm.instructions import Opcode
from aayu.runtime.vm.exceptions import KernelError
from aayu.runtime.vm.result import ResultStatus
import time''', import_stmt)

# Let's map widget IDs back to string names
widget_map_code = '''
WIDGET_TYPE_NAMES = {
    0: "Text",
    1: "Button",
    2: "Input",
    8: "Page",
    9: "Column",
}
'''
if "WIDGET_TYPE_NAMES" not in content:
    content = content.replace("class Interpreter:", widget_map_code + "\nclass Interpreter:")

# Initialize render tree in __init__
init_old = '''    def __init__(self, vm):
        self.vm = vm'''
init_new = '''    def __init__(self, vm):
        self.vm = vm
        self.render_tree = RenderTree()
        self.node_stack = []'''
content = content.replace(init_old, init_new)

# Replace BUILD_WIDGET
build_old = '''            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                if widget_type == 0:
                    print(props)'''

build_new = '''            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                
                type_name = WIDGET_TYPE_NAMES.get(widget_type, f"Unknown_{widget_type}")
                
                # Create node
                # props can be string or dict. we'll store in 'value' if string
                node_props = props if isinstance(props, dict) else {"value": props}
                node = RenderNode(type_name, props=node_props)
                
                if type_name == "Page":
                    self.render_tree.root = node
                    self.node_stack.clear()
                    self.node_stack.append(node)
                else:
                    if self.node_stack:
                        self.node_stack[-1].add_child(node)
                    else:
                        # Fallback if no page
                        self.render_tree.root = node
                        self.node_stack.append(node)'''
                        
content = content.replace(build_old, build_new)

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
