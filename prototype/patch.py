import sys
with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/vm.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_unwrap = \"py_args = [a.value if hasattr(a, 'value') else a for a in args]\"
new_unwrap = \"py_args = [a.to_python() if hasattr(a, 'to_python') else a for a in args]\"

if old_unwrap in text:
    text = text.replace(old_unwrap, new_unwrap)
    with open('d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/vm.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Fixed py_args unwrap in vm.py')
else:
    print('Could not find old_unwrap')
