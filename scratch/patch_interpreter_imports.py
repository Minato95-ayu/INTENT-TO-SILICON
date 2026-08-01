with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = "from aayu.runtime.ui.render_tree import RenderTree, RenderNode\n" + content

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
