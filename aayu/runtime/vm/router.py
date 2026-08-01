import time
from dataclasses import dataclass, field
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

@dataclass
class Route:
    name: str
    path: str
    params: dict = field(default_factory=dict)
    query: dict = field(default_factory=dict)
    state: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

class UIRouter:
    def __init__(self, vm):
        self.vm = vm
        self.history = []
        self.current_route = None

    def navigate(self, target: str, params: dict):
        path = "/" + target.lower()
        if target.lower() == "home":
            path = "/"
            
        route = Route(name=target, path=path, params=params)
        self.history.append(route)
        self.current_route = route
        
        print(f"[UIRouter] Navigated to {target} with {params}")
        
        # Pass params to VM state for the page
        self.vm.state["props"] = params
        self.vm.state["route"] = {"params": params, "name": target, "path": path, "query": {}}
        
        # Execute the page in the VM
        self.vm.call_action_by_name(target)
        
        # Dispatch event to Renderer
        if self.vm.interpreter and hasattr(self.vm.interpreter, 'render_tree') and self.vm.interpreter.render_tree:
            self.vm.interpreter.render_tree.dispatch_navigation(route)

    def back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.current_route = self.history[-1]
            print(f"[UIRouter] Back to {self.current_route.name}")
            
            # Pass params and re-execute
            self.vm.state["props"] = self.current_route.params
            self.vm.state["route"] = {"params": self.current_route.params, "name": self.current_route.name, "path": self.current_route.path, "query": self.current_route.query}
            self.vm.call_action_by_name(f"__PAGE_START_{self.current_route.name}")
            
            if self.vm.interpreter and hasattr(self.vm.interpreter, 'render_tree') and self.vm.interpreter.render_tree:
                self.vm.interpreter.render_tree.dispatch_navigation(self.current_route)
            
class APIRouter:
    def __init__(self, vm, port=8080):
        self.vm = vm
        self.port = port
        self.routes = {} # { "/api/login": { "post": bytecode_address } }
        self.server = None
        self.thread = None

    def register_route(self, path: str, methods_meta: list):
        if path not in self.routes:
            self.routes[path] = {}
        for meta in methods_meta:
            method = meta["method"].lower()
            addr = meta["target_address"]
            self.routes[path][method] = addr
            print(f"[Router] Registered route {method.upper()} {path} -> addr 0x{addr:04X}")

    def start(self):
        pass # APIRouter stub

    def stop(self):
        pass # APIRouter stub
