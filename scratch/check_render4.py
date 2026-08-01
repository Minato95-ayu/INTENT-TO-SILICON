
from aayu.runtime.vm.vm import VirtualMachine
from aayu.runtime.renderers.web_renderer import WebRenderer

with open("app.aayuc", "rb") as f:
    bytecode = f.read()

try:
    vm = VirtualMachine()
    vm.load(bytecode, [], {})
    vm.execute()

    renderer = WebRenderer(vm.event_queue, port=3000)
    html = renderer._render_node_to_html(vm.interpreter.render_tree.root)
    print(html)
except Exception as e:
    import traceback
    traceback.print_exc()

