"""
=============================================================================
FILE: method_calls.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

from ...ast_nodes import Node, MethodCallNode, CallNode

class MethodCallLoweringPass:
    def transform(self, node: Node) -> Node:
        if isinstance(node, MethodCallNode):
            # Transform obj.method(arg) -> __method_methodname(obj, arg)
            new_name = f"__method_{node.method_name}"
            # The obj is the first argument
            new_args = [node.object_node] + node.arguments
            # Transform arguments as well
            transformed_args = [self.transform(a) for a in new_args]
            return CallNode(name=new_name, arguments=transformed_args)
            
        # Recurse into children
        if hasattr(node, '__dict__'):
            for k, v in vars(node).items():
                if isinstance(v, Node):
                    setattr(node, k, self.transform(v))
                elif isinstance(v, list):
                    setattr(node, k, [self.transform(x) if isinstance(x, Node) else x for x in v])
        return node
