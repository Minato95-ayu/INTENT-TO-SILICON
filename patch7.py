import sys
with open('build_entry.py', 'r', encoding='utf-8') as f:
    code = f.read()

if 'import runtime.renderers.web_renderer' not in code:
    code = code.replace(
        "import tools.commands.version",
        "import tools.commands.version\nimport runtime.renderers.web_renderer"
    )
    with open('build_entry.py', 'w', encoding='utf-8') as f:
        f.write(code)