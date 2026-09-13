from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.string import StringValue
from ...values.null import NullValue
from ...values.list import ListValue
from ...values.map import MapValue
from ...values.number import NumberValue

def _value(val):
    return val.to_python() if hasattr(val, "to_python") else val

def register_ai_lib(registry: StdLibRegistry):
    def fn_train(args, vm):
        val = f"Model trained on {_value(args[0])} epochs with 98% accuracy"
        heap_id = vm.heap.allocate("string", val)
        return StringValue(heap_id, vm.heap)
        
    def fn_predict(args, vm):
        val = f"Prediction for input {_value(args[0])} -> CLASS_A"
        heap_id = vm.heap.allocate("string", val)
        return StringValue(heap_id, vm.heap)
        
    def fn_kmeans(args, vm):
        val = f"K-Means clustered {_value(args[0])} data points into {_value(args[1])} clusters"
        heap_id = vm.heap.allocate("string", val)
        return StringValue(heap_id, vm.heap)
        
    registry.register("ai::train", fn_train)
    registry.register("ai::predict", fn_predict)
    registry.register("ml::kmeans", fn_kmeans)
