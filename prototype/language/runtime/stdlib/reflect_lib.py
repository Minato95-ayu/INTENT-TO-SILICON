from ..values.base import RuntimeValue
from ..values.string import StringValue
from ..values.list import ListValue
from ..values.map import MapValue
from ..values.null import NullValue

def _make_string(vm, text: str) -> RuntimeValue:
    obj = vm.memory.heap.allocate("string", text)
    from ..values.string import StringValue
    return StringValue(obj.id, vm.memory.heap)

def reflect_type_of(args, vm) -> RuntimeValue:
    if not args:
        return NullValue()
    return _make_string(vm, args[0].type_name())

def reflect_attributes_of(args, vm) -> RuntimeValue:
    if not args:
        raise Exception("reflect::attributes_of requires 1 argument")
    
    val = args[0]
    type_name = val.type_name()
    
    attrs = []
    if type_name == "Map":
        attrs = list(val.elements.keys())
    elif type_name == "Module":
        attrs = list(val.exports.keys())
    elif type_name == "Function":
        # Functions don't currently expose user-defined attributes in AAYU,
        # but could expose metadata keys if desired. We'll return empty for now.
        pass
        
    attrs_list = [_make_string(vm, a) for a in attrs]
    obj = vm.memory.heap.allocate("list", attrs_list)
    from ..values.list import ListValue
    return ListValue(obj.id, vm.memory.heap)

def reflect_module_of(args, vm) -> RuntimeValue:
    if not args:
        raise Exception("reflect::module_of requires 1 argument")
        
    val = args[0]
    if hasattr(val, "reflection_info") and val.reflection_info:
        module_name = val.reflection_info.module
        if module_name:
            return _make_string(vm, module_name)
    
    return NullValue()

def reflect_inspect(args, vm) -> RuntimeValue:
    if not args:
        raise Exception("reflect::inspect requires 1 argument")
        
    val = args[0]
    meta_map = {
        "type": _make_string(vm, val.type_name())
    }
    
    if hasattr(val, "name"):
        meta_map["name"] = _make_string(vm, val.name)
        
    if hasattr(val, "reflection_info") and val.reflection_info:
        info = val.reflection_info
        if info.module:
            meta_map["module"] = _make_string(vm, info.module)
        if info.visibility:
            meta_map["visibility"] = _make_string(vm, info.visibility)
        from ..values.boolean import BooleanValue
        meta_map["is_exported"] = BooleanValue(info.is_exported)
        
        from ..values.number import NumberValue
        if info.parameter_count is not None:
            meta_map["parameter_count"] = NumberValue(float(info.parameter_count))
            
    obj = vm.memory.heap.allocate("map", meta_map)
    from ..values.map import MapValue
    return MapValue(obj.id, vm.memory.heap)

def register_reflect_lib(registry):
    registry.register("reflect_type_of", reflect_type_of)
    registry.register("reflect_attributes_of", reflect_attributes_of)
    registry.register("reflect_module_of", reflect_module_of)
    registry.register("reflect_inspect", reflect_inspect)
