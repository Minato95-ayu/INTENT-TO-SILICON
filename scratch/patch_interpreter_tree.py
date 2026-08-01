with open('runtime/vm/interpreter.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_build = '''                if type_name == "Page":
                    self.render_tree.root = node
                    self.node_stack.clear()
                    self.node_stack.append(node)
                else:
                    if self.node_stack:
                        self.node_stack[-1].add_child(node)
                    else:
                        # Fallback if no page
                        self.render_tree.root = node
                        self.node_stack.append(node)'''

new_build = '''                if type_name in ["Page", "Column", "Row"]:
                    # All accumulated unparented nodes become children
                    for child in self.node_stack:
                        node.add_child(child)
                    self.node_stack.clear()
                    self.node_stack.append(node)
                    if type_name == "Page":
                        self.render_tree.root = node
                else:
                    self.node_stack.append(node)'''
                        
content = content.replace(old_build, new_build)

with open('runtime/vm/interpreter.py', 'w', encoding='utf-8') as f:
    f.write(content)
