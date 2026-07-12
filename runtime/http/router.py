class RouteNode:
    def __init__(self):
        self.children = {}
        self.handlers = {} # method -> handler func
        self.param_name = None # e.g. 'id' for '{id}'
        self.is_param = False

class Router:
    def __init__(self):
        self.root = RouteNode()

    def add_route(self, method: str, path: str, handler):
        parts = [p for p in path.split('/') if p]
        current = self.root
        
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                # Parameterized route node
                param_name = part[1:-1]
                if '*' not in current.children:
                    node = RouteNode()
                    node.is_param = True
                    node.param_name = param_name
                    current.children['*'] = node
                current = current.children['*']
            else:
                if part not in current.children:
                    current.children[part] = RouteNode()
                current = current.children[part]
                
        current.handlers[method.upper()] = handler

    def find_route(self, method: str, path: str):
        parts = [p for p in path.split('/') if p]
        current = self.root
        params = {}
        
        for part in parts:
            if part in current.children:
                current = current.children[part]
            elif '*' in current.children:
                current = current.children['*']
                params[current.param_name] = part
            else:
                return None, None
                
        handler = current.handlers.get(method.upper())
        if not handler:
            return None, None
            
        return handler, params
