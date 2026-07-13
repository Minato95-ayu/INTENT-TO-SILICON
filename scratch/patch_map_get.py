import re

with open('runtime/vm/handlers/collections_ops.py', 'r', encoding='utf-8') as f:
    text = f.read()

new_func = """
def handle_map_get(vm, frame):
    coll = frame.stack.pop()
    key = frame.stack.pop()
    
    from ..values.list import ListValue
    from ..values.map import MapValue
    from ..values.number import NumberValue
    from ..values.string import StringValue
    from ..values.null import NullValue
    
    if isinstance(coll, ListValue):
        if not isinstance(key, NumberValue):
            vm._raise_runtime_error("List index must be a number.")
        idx = int(key.value)
        elements = coll._get_payload()
        if 0 <= idx < len(elements):
            frame.stack.append(elements[idx])
        else:
            frame.stack.append(NullValue())
    elif isinstance(coll, MapValue):
        if not isinstance(key, StringValue):
            vm._raise_runtime_error("Map key must be a string.")
        k = key.value
        pairs = coll._get_payload()
        for pair in pairs:
            if pair[0] == k:
                frame.stack.append(pair[1])
                return
        frame.stack.append(NullValue())
    else:
        vm._raise_runtime_error("Cannot get item from non-collection.")
"""

with open('runtime/vm/handlers/collections_ops.py', 'a', encoding='utf-8') as f:
    f.write(new_func)
