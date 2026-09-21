with open('runtime/vm/validator.py', 'r') as f:
    code = f.read()

# I want to add some print statements in validator.py
old = 'raise InvalidBytecodeError(f"Incompatible stack depths at merge point: expected {visited[state_key]}, got {depth}", ip)'
new = 'print(f"DEBUG: op={Opcode(opcode).name} ip={ip} visited={visited[state_key]} depth={depth}"); ' + old
code = code.replace(old, new)

with open('runtime/vm/validator.py', 'w') as f:
    f.write(code)
