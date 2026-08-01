import re
from ..registry import StdLibRegistry
from ...values.string import StringValue
from ...values.boolean import BooleanValue

def register_regex_lib(registry: StdLibRegistry):
    def fn_match(args, vm):
        try:
            pattern = args[0].to_python()
            string = args[1].to_python()
            return BooleanValue(bool(re.match(pattern, string)))
        except Exception:
            return BooleanValue(False)
            
    registry.register("regex::match", fn_match)
