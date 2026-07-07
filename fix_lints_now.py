import re
def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # no-explicit-any
    content = re.sub(r'\bany\b', 'unknown', content)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

