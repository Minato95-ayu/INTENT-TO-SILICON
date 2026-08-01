with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

import re

old_build_widget = '''            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                # Do nothing until Phase 7.2'''

new_build_widget = '''            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                if widget_type == 0:
                    print(props)'''

content = content.replace(old_build_widget, new_build_widget)

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
