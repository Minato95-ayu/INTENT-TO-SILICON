from ast_nodes import ImportNode
from resolver.symbols import ModuleSymbol
from ..base import ASTVisitorPass

class ImportBindingPass(ASTVisitorPass):
    def __init__(self):
        super().__init__("ImportBindingPass")
        
    def run(self, context):
        self.context = context
        self.current_scope = context.symbol_tables[context.current_module]
        return super().run(context)
        
    def visit_ImportNode(self, node: ImportNode):
        dep_table = self.context.symbol_tables.get(node.module_name)
        if dep_table:
            # If selective imports exist, we bind individual symbols
            if getattr(node, 'selective_imports', None) is not None:
                for sym_name, sym_alias in node.selective_imports.items():
                    target_sym = dep_table.lookup(sym_name, current_only=True)
                    if not target_sym:
                        self.context.diagnostics.error(f"Cannot import '{sym_name}' from '{node.module_name}'. It does not exist.", self.context.current_module, node=node)
                        continue
                        
                    is_exported = getattr(target_sym, 'is_exported', False)
                    visibility = getattr(target_sym, 'visibility', 'private')
                    
                    if not is_exported and visibility != 'public':
                        self.context.diagnostics.error(f"Cannot import private symbol '{sym_name}' from '{node.module_name}'.", self.context.current_module, node=node)
                        continue
                        
                    bind_name = sym_alias if sym_alias else sym_name
                    # We create a shallow proxy symbol or just bind the original.
                    # Since dictionary key matters for lookup:
                    if bind_name in self.current_scope.symbols:
                        self.context.diagnostics.error(f"Cannot import '{sym_name}' as '{bind_name}'. Name already in use.", self.context.current_module, node=node)
                    else:
                        self.current_scope.symbols[bind_name] = target_sym
                node.symbol = None # Selective imports don't bind a module symbol
            else:
                bind_name = getattr(node, 'alias', None)
                if not bind_name:
                    # By default, use the last part of the module path or the full path?
                    # Let's keep it as module_name for backward compatibility.
                    bind_name = node.module_name
                mod_sym = ModuleSymbol(bind_name, self.current_scope, dep_table)
                self.current_scope.define(mod_sym)
                node.symbol = mod_sym
        else:
            self.context.diagnostics.error(f"Module '{node.module_name}' symbol table not found during import binding.", self.context.current_module)
