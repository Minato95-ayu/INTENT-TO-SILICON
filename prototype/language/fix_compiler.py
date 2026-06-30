import re

with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/compiler.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    if "Opcode.BUILD_LIST" in line:
        line = line.replace("BUILD_LIST", "MAKE_LIST")
    if "Opcode.BUILD_MAP" in line:
        line = line.replace("BUILD_MAP", "MAKE_MAP")
    
    new_lines.append(line)
    i += 1

text = "".join(new_lines)

# Fix CALL_TASK blocks safely using a more precise regex.
def fix_call_task(match):
    func_def = match.group(1)
    body = match.group(2)
    load_block = match.group(3)
    call_block = match.group(4)
    
    if "fn_idx = self._add_name(" in body:
        # If there are multiple fn_idx blocks, don't break them!
        pass
        
    return f"{func_def}\n{load_block}\n{body}\n{call_block}"

# We will just write a custom parser for each visit method instead of regex, it's safer.
def fix_compiler_methods(text):
    methods = text.split("    def visit_")
    out = [methods[0]]
    for m in methods[1:]:
        m_full = "    def visit_" + m
        if "Opcode.CALL_TASK" in m_full and "fn_idx = self._add_name(" in m_full:
            # Find the load block
            # It usually looks like:
            #         fn_idx = self._add_name("something")
            #         self._emit(Opcode.LOAD_VAR, fn_idx)
            load_idx = m_full.find("        fn_idx = self._add_name(")
            if load_idx != -1:
                end_load_idx = m_full.find(")", m_full.find("Opcode.LOAD_VAR, fn_idx", load_idx)) + 1
                if end_load_idx != 0:
                    load_block = m_full[load_idx:end_load_idx]
                    
                    # Remove it from where it is
                    m_full = m_full[:load_idx] + m_full[end_load_idx:]
                    # Insert it right after the def line
                    def_end = m_full.find(":\n") + 2
                    m_full = m_full[:def_end] + load_block + "\n" + m_full[def_end:]
                    
        # Special case for RunNode which uses name_idx
        if "def visit_RunNode" in m_full:
            load_idx = m_full.find("        name_idx = self._add_name(node.name)")
            if load_idx != -1:
                end_load_idx = m_full.find(")", m_full.find("Opcode.LOAD_VAR, name_idx", load_idx)) + 1
                if end_load_idx != 0:
                    load_block = m_full[load_idx:end_load_idx]
                    m_full = m_full[:load_idx] + m_full[end_load_idx:]
                    def_end = m_full.find(":\n") + 2
                    m_full = m_full[:def_end] + load_block + "\n" + m_full[def_end:]

        out.append(m_full)
    return "".join(out)

fixed_text = fix_compiler_methods(text)

with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/compiler.py', 'w', encoding='utf-8') as f:
    f.write(fixed_text)

print("Fixed compiler.py")


# Append visit_ShowNode to compiler.py
with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/compiler.py', 'a', encoding='utf-8') as f:
    f.write('''
    def visit_ShowNode(self, node):
        fn_idx = self._add_name('print')
        self._emit(Opcode.LOAD_VAR, fn_idx)
        self.visit(node.expression)
        self._emit(Opcode.CALL, 1)
        self._emit(Opcode.POP)
''')