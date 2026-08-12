import os

def dump_ast(ast, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ast.dump"), "w") as f:
        # Simple tree printer
        def print_node(n, indent=0):
            if not n: return
            f.write("  " * indent + str(type(n).__name__) + "\n")
            if hasattr(n, "__dict__"):
                for k, v in n.__dict__.items():
                    if k in ['line', 'column', 'span']: continue
                    if isinstance(v, list):
                        for item in v:
                            print_node(item, indent + 1)
                    else:
                        print_node(v, indent + 1)
        print_node(ast)

def dump_hir(hir, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "hir.dump"), "w") as f:
        def print_hir(n, indent=0):
            if not n: return
            f.write("  " * indent + str(type(n).__name__) + "\n")
            if hasattr(n, "__dict__"):
                for k, v in n.__dict__.items():
                    if isinstance(v, list):
                        for item in v:
                            print_hir(item, indent + 1)
                    elif hasattr(v, "__dict__"):
                        print_hir(v, indent + 1)
                    else:
                        f.write("  " * (indent + 1) + f"{k}: {v}\n")
        print_hir(hir)

def dump_mir(mir, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "mir.dump"), "w") as f:
        for func in mir.functions:
            f.write(f"Function {func.name}:\n")
            for block in func.blocks:
                f.write(f"  {block.id}:\n")
                for instr in block.instructions:
                    f.write(f"    {instr}\n")

def dump_cfg_dot(mir, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "cfg.dot"), "w") as f:
        f.write("digraph CFG {\n")
        f.write("  node [shape=box];\n")
        for func in mir.functions:
            for block in func.blocks:
                label = f"{block.id}\\n"
                for instr in block.instructions:
                    label += f"{instr}\\n"
                f.write(f'  "{block.id}" [label="{label}"];\n')
                
                for succ in block.successors:
                    f.write(f'  "{block.id}" -> "{succ.id}";\n')
        f.write("}\n")

def dump_dominator(mir, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "dominator.dump"), "w") as f:
        for func in mir.functions:
            f.write(f"Function {func.name} Dominance:\n")
            if hasattr(func, 'analysis'):
                idom = func.analysis.get('idom', {})
                df = func.analysis.get('df', {})
                dom_tree = func.analysis.get('dom_tree', {})
                f.write("  Immediate Dominators (idom):\n")
                for k, v in idom.items():
                    f.write(f"    {k} -> {v}\n")
                f.write("  Dominator Tree Children:\n")
                for k, v in dom_tree.items():
                    f.write(f"    {k}: {v}\n")
                f.write("  Dominance Frontiers (DF):\n")
                for k, v in df.items():
                    f.write(f"    {k}: {list(v)}\n")

def dump_ssa(mir, out_dir="tests/conformance"):
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "ssa.dump"), "w") as f:
        for func in mir.functions:
            f.write(f"Function {func.name}:\n")
            for block in func.blocks:
                f.write(f"  {block.id}:\n")
                for instr in block.instructions:
                    # Format PHI beautifully
                    if instr.opcode.name == "PHI":
                        args = ", ".join([f"{b}: {r}" for b, r in instr.operands])
                        f.write(f"    {instr.dest} = phi({args})\n")
                    else:
                        f.write(f"    {instr}\n")
