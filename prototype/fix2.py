import re

with open('aayu_language/parser.py', 'r') as f:
    lines = f.readlines()

out = []
in_bad_block = False

for l in lines:
    if l.startswith("    def parse_create(self):") or l.startswith("        def parse_create(self):"):
        in_bad_block = True
    
    if in_bad_block and l.startswith("    def parse_map_declaration(self)"):
        in_bad_block = False
        
    if in_bad_block and l.startswith("    "):
        # remove exactly 4 spaces
        out.append(l[4:])
    else:
        out.append(l)

with open('aayu_language/parser.py', 'w') as f:
    f.writelines(out)
