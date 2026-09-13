import re
with open("compiler/ir/cfg_builder.py", "r") as f:
    content = f.read()

replacement = """        if isinstance(hir, HIRActionDecl):
            # Process body in a new CFG Context
            action_cfg = CFG()
            old_cfg = self.current_cfg
            old_block = self.current_block
            
            self.current_cfg = action_cfg
            self.current_block = action_cfg.entry_block
            
            for stmt in hir.body:
                self._lower_hir(stmt)
                
            self.current_cfg = old_cfg
            self.current_block = old_block
            
            return self._emit("ACTION_DECL", [hir.name, action_cfg, hir.args])
            
        elif isinstance(hir, HIRIf):"""

content = re.sub(r'        if isinstance\(hir, HIRActionDecl\):\n\s*return None\n\s*elif isinstance\(hir, HIRIf\):', replacement, content, flags=re.DOTALL)
with open("compiler/ir/cfg_builder.py", "w") as f:
    f.write(content)
