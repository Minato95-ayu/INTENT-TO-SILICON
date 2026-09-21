with open('runtime/vm/validator.py', 'r') as f:
    code = f.read()

old = 'visited[state_key] = depth\n            opcode = bytecode[ip]'
new = 'visited[state_key] = depth\n            opcode = bytecode[ip]\n            print(f"[{ip}] depth={depth} opcode={opcode}")'
code = code.replace(old, new)

with open('runtime/vm/validator.py', 'w') as f:
    f.write(code)
