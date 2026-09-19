# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

def _print_tree_recursive(graph, node, prefix="", is_last=True):
    connector = "└── " if is_last else "├── "
    print(f"{prefix}{connector}{node}")
    
    children = graph.get(node, [])
    for i, child in enumerate(children):
        is_last_child = i == (len(children) - 1)
        new_prefix = prefix + ("    " if is_last else "│   ")
        _print_tree_recursive(graph, child, new_prefix, is_last_child)

class TreePrinter:
    """Prints dependency graph in ASCII format."""
    
    @staticmethod
    def print_tree(root_name: str, dependency_graph: dict):
        print(root_name)
        children = dependency_graph.get(root_name, [])
        for i, child in enumerate(children):
            is_last = i == (len(children) - 1)
            _print_tree_recursive(dependency_graph, child, "", is_last)
