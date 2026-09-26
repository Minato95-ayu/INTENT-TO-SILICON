import sys

with open('runtime/session/manager.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    'if self.vm.interpreter.render_tree and self.vm.interpreter.render_tree.root:',
    '''print("DIRTY CHECK! render_tree:", self.vm.interpreter.render_tree)
                    if self.vm.interpreter.render_tree and self.vm.interpreter.render_tree.root:
                        print("ROOT EXISTS:", self.vm.interpreter.render_tree.root)'''
)

with open('runtime/session/manager.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("PATCHED")