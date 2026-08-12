from aayu.compiler.ir import Opcode
from aayu.compiler.ast_nodes import InsertNode, FindNode, UpdateNode, DeleteNode
from aayu.runtime.values.list import ListValue
from aayu.runtime.values.map import MapValue
from aayu.runtime.values.string import StringValue
from aayu.runtime.values.number import NumberValue
from aayu.runtime.values.null import NullValue

class AAYURuntimeError(Exception):
    pass

def _get_db_runtime(vm):
    db_runtime = vm.runtime_manager.get_runtime("DatabaseRuntime")
    if not db_runtime:
        raise AAYURuntimeError("DatabaseRuntime is not initialized.")
    return db_runtime

def handle_storage(opcode, current_frame, vm):
    db_runtime = _get_db_runtime(vm)
    
    if opcode == Opcode.DB_INSERT:
        fields_map = current_frame.stack.pop()
        model_name = current_frame.stack.pop()
        
        ast_node = InsertNode(model_name.to_python(), fields_map.to_python())
        db_runtime.engine.execute_query_ast(ast_node)
        current_frame.stack.append(NullValue())
        
    elif opcode == Opcode.DB_FIND:
        model_name = current_frame.stack.pop()
        
        ast_node = FindNode(model_name.to_python())
        res = db_runtime.engine.execute_query_ast(ast_node)
        
        aayu_list = []
        if res:
            for row in res:
                py_dict = {}
                for k, v in row.items():
                    if isinstance(v, (int, float)):
                        py_dict[str(k)] = NumberValue(v)
                    else:
                        s_obj = vm.memory.heap.allocate("string", str(v))
                        py_dict[str(k)] = StringValue(s_obj.id, vm.memory.heap)
                map_obj = vm.memory.heap.allocate("map", py_dict)
                aayu_list.append(MapValue(map_obj.id, vm.memory.heap))
            
        list_obj = vm.memory.heap.allocate("list", aayu_list)
        current_frame.stack.append(ListValue(list_obj.id, vm.memory.heap))
        
    elif opcode == Opcode.DB_UPDATE:
        fields_map = current_frame.stack.pop()
        model_name = current_frame.stack.pop()
        
        ast_node = UpdateNode(model_name.to_python(), fields_map.to_python())
        db_runtime.engine.execute_query_ast(ast_node)
        current_frame.stack.append(NullValue())
        
    elif opcode == Opcode.DB_DELETE:
        model_name = current_frame.stack.pop()
        
        ast_node = DeleteNode(model_name.to_python())
        db_runtime.engine.execute_query_ast(ast_node)
        current_frame.stack.append(NullValue())
    
    return False
