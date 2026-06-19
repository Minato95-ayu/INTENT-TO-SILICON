import os

with open('aayu_language/parser.py', 'r') as f:
    lines = f.readlines()

with open('append_parser.txt', 'r') as f:
    append_lines = f.readlines()

out = []
appended = False

for l in lines:
    if 'def parse_map_declaration' in l and not appended:
        for al in append_lines:
            if al.strip():
                out.append('    ' + al)
            else:
                out.append(al)
        appended = True
    
    # Do not include the old unindented definitions at the bottom!
    if l.startswith("def parse_entity_declaration") or l.startswith("    def parse_entity_declaration") and "def parse_entity_declaration(self):" == l.strip():
        # we will stop copying lines if we hit the old ones
        # actually, just let's filter out the bottom block if we know where it is
        pass
        
    out.append(l)

# to be safe, filter the bottom ones
# the old appended lines started from the end
final_out = []
skip = False
for l in out:
    if "def parse_entity_declaration" in l and not l.startswith("    def parse_entity_declaration"):
        skip = True
    if not skip:
        final_out.append(l)

with open('aayu_language/parser.py', 'w') as f:
    f.writelines(final_out)
