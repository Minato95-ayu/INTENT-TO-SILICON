from ..registry import StdLibRegistry
from ...values.boolean import BooleanValue

def register_testing_lib(registry: StdLibRegistry):
    def fn_assert_eq(args, vm):
        v1 = args[0]
        v2 = args[1]
        
        # Proper deep comparison
        if hasattr(v1, 'to_python') and hasattr(v2, 'to_python'):
            if v1.to_python() == v2.to_python():
                return BooleanValue(True)
        elif hasattr(v1, 'value') and hasattr(v2, 'value'):
            if v1.value == v2.value:
                return BooleanValue(True)
                
        return BooleanValue(False)
        
    registry.register("testing::assert_eq", fn_assert_eq)
