with open("runtime/stdlib/modules/ml.py", "a") as f:
    f.write("""
from ..registry import StdLibRegistry
from ...values.base import RuntimeValue
from ...values.number import NumberValue
from ...values.list import ListValue
from ...values.map import MapValue

def py_to_aayu(py_val, vm):
    if isinstance(py_val, (int, float)): return NumberValue(float(py_val))
    if isinstance(py_val, list):
        l = [py_to_aayu(x, vm) for x in py_val]
        obj = vm.heap.allocate("list", l)
        return ListValue(obj, vm.heap)
    return NumberValue(0.0)

def aayu_to_py(val):
    if hasattr(val, "to_python"): return val.to_python()
    return val

def register_ml_lib(registry: StdLibRegistry):
    def fn_kmeans_fit(args, vm):
        try:
            data = aayu_to_py(args[0])
            k = int(aayu_to_py(args[1])) if len(args) > 1 else 3
            max_iters = int(aayu_to_py(args[2])) if len(args) > 2 else 100
            model_id = ml_kmeans_fit(data, k, max_iters)
            return NumberValue(model_id)
        except Exception:
            return NumberValue(-1)

    def fn_kmeans_predict(args, vm):
        try:
            model_id = int(aayu_to_py(args[0]))
            point = aayu_to_py(args[1])
            cluster = ml_kmeans_predict(model_id, point)
            return NumberValue(cluster)
        except Exception:
            return NumberValue(-1)
            
    def fn_linear_regression_fit(args, vm):
        try:
            X = aayu_to_py(args[0])
            y = aayu_to_py(args[1])
            model_id = ml_linear_regression_fit(X, y)
            return NumberValue(model_id)
        except Exception:
            return NumberValue(-1)
            
    def fn_linear_regression_predict(args, vm):
        try:
            model_id = int(aayu_to_py(args[0]))
            X = aayu_to_py(args[1])
            predictions = ml_linear_regression_predict(model_id, X)
            return py_to_aayu(predictions, vm)
        except Exception:
            return py_to_aayu([], vm)

    registry.register("ml::kmeans_fit", fn_kmeans_fit)
    registry.register("ml::kmeans_predict", fn_kmeans_predict)
    registry.register("ml::linear_regression_fit", fn_linear_regression_fit)
    registry.register("ml::linear_regression_predict", fn_linear_regression_predict)
""")
