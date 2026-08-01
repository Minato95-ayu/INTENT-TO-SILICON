import re

with open('aayu/runtime/vm/instructions.py', 'r') as f:
    content = f.read()
    
c_header = ["#ifndef AAYU_OPCODES_H", "#define AAYU_OPCODES_H", "", "typedef enum {"]

for line in content.split('\n'):
    line = line.strip()
    if not line or line.startswith('#') or line.startswith('class') or line.startswith('\"\"\"'):
        continue
    
    match = re.match(r'([A-Z0-9_]+)\s*=\s*(0x[0-9A-Fa-f]+|[0-9]+)', line)
    if match:
        name = match.group(1)
        val = match.group(2)
        c_header.append(f"    OP_{name} = {val},")

c_header.append("} AayuOpcode;")
c_header.append("")
c_header.append("#endif")

with open('runtime/native/opcodes.h', 'w') as out:
    out.write('\n'.join(c_header) + '\n')
