with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_add_sub = '''            elif opcode == Opcode.SUB:
                self.vm.registers.ip += 1
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a - b)'''

new_add_sub = '''            elif opcode == Opcode.SUB:
                self.vm.registers.ip += 1
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a - b)
                
            elif opcode == Opcode.MUL:
                self.vm.registers.ip += 1
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                self.vm.value_stack.push(a * b)
                
            elif opcode == Opcode.DIV:
                self.vm.registers.ip += 1
                b = self.vm.value_stack.pop()
                a = self.vm.value_stack.pop()
                if b == 0:
                    raise KernelError("Division by zero")
                self.vm.value_stack.push(a / b)'''
content = content.replace(old_add_sub, new_add_sub)

old_load_state = '''            elif opcode == Opcode.LOAD_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.state.get(name, None)
                self.vm.value_stack.push(val)'''

new_load_state = '''            elif opcode == Opcode.LOAD_STATE:
                idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                name = self.vm.constant_pool[idx]
                val = self.vm.state.get(name, None)
                self.vm.value_stack.push(val)
                
            elif opcode == Opcode.BUILD_WIDGET:
                widget_type = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
                self.vm.registers.ip += 3
                props = self.vm.value_stack.pop()
                print(props)
                
            elif opcode == Opcode.PRINT:
                self.vm.registers.ip += 1
                val = self.vm.value_stack.pop()
                print(val)'''

content = content.replace(old_load_state, new_load_state)

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
