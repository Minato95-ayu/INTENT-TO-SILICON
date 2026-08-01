with open('tools/commands/run.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_load = '''        vm = VirtualMachine()
        vm.load(program.bytecode, program.constant_pool.values())'''

new_load = '''        vm = VirtualMachine()
        vm.load(program.bytecode, program.constant_pool.values(), program.action_addresses)'''

content = content.replace(old_load, new_load)

with open('tools/commands/run.py', 'w', encoding='utf-8') as f:
    f.write(content)
