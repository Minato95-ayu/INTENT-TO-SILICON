import sqlite3
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.boolean import BooleanValue
from ...values.number import NumberValue

def create_string(vm, text):
    obj = vm.memory.heap.allocate("string", text)
    return StringValue(obj.id, vm.memory.heap)

def py_to_aayu(py_val, vm):
    if isinstance(py_val, str): return create_string(vm, py_val)
    if isinstance(py_val, (int, float)): return NumberValue(float(py_val))
    if isinstance(py_val, bool): return BooleanValue(py_val)
    return NullValue()

def register_database_lib(registry: StdLibRegistry):
    connections = {}
    
    def fn_connect(args, vm):
        try:
            path = args[0].to_python()
            conn = sqlite3.connect(path)
            conn.row_factory = sqlite3.Row
            cid = str(id(conn))
            connections[cid] = conn
            return create_string(vm, cid)
        except Exception:
            return NullValue()
            
    def fn_query(args, vm):
        try:
            cid = args[0].to_python()
            query = args[1].to_python()
            conn = connections.get(cid)
            if not conn: return NullValue()
            
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            
            result_list = []
            for row in rows:
                d = {k: py_to_aayu(row[k], vm) for k in row.keys()}
                obj_m = vm.memory.heap.allocate("map", d)
                result_list.append(MapValue(obj_m.id, vm.memory.heap))
            obj_l = vm.memory.heap.allocate("list", result_list)
            return ListValue(obj_l.id, vm.memory.heap)
        except Exception as e:
            return NullValue()
            
    registry.register("db::connect", fn_connect)
    registry.register("db::query", fn_query)
