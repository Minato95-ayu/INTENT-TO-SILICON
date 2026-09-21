with open('runtime/vm/validator.py', 'r') as f:
    code = f.read()

old = 'if visited[state_key] != depth:'
new = 'if True:\n                #print(f"[{ip}] depth {depth}")\n                pass\n            ' + old
code = code.replace(old, new)

old2 = 'visited[state_key] = depth'
new2 = 'print(f"[{ip}] depth {depth} opcode={opcode}"); ' + old2
code = code.replace(old2, new2)

with open('runtime/vm/validator.py', 'w') as f:
    f.write(code)
