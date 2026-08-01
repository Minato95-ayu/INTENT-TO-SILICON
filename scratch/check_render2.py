
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.db.sqlite_backend import SQLiteBackend
from aayu.runtime.api.router import APIRouter
from aayu.runtime.renderers.web_renderer import WebRenderer
import json

with open("app.aayuc", "rb") as f:
    bytecode = f.read()
    
vm = VirtualMachine(bytecode)
db = SQLiteBackend("app.db")
router = APIRouter()
vm.register_system_api("db", db)
vm.register_system_api("router", router)

vm.run()

renderer = WebRenderer(vm.event_queue, port=3000)
html = renderer._render_node_to_html(vm.render_tree)
print(html)

