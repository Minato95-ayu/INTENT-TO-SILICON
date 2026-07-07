import os

base_dir = r"d:\intent-to-silicon-research\INTENT-TO-SILICON\prototype\language\runtime\stdlib\modules"

def update_file(filename, replacements):
    filepath = os.path.join(base_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Updating files...")

update_file("file_lib.py", [
    ('registry.register("file::mkdir", fn_mkdir)', 'registry.register("file::mkdir", fn_mkdir)\n    registry.register("directory::create", fn_mkdir)')
])

update_file("json_lib.py", [
    ('registry.register("json::encode", fn_encode)', 'registry.register("json::encode", fn_encode)\n    registry.register("json::stringify", fn_encode)'),
    ('registry.register("json::decode", fn_decode)', 'registry.register("json::decode", fn_decode)\n    registry.register("json::parse", fn_decode)')
])

update_file("time_lib.py", [
    ('registry.register("time::timestamp", fn_timestamp)', 'registry.register("time::timestamp", fn_timestamp)\n    \n    def fn_date_format(args, vm):\n        if len(args) < 2: return NullValue()\n        date_str = args[0].to_python()\n        fmt = args[1].to_python()\n        try:\n            dt = datetime.datetime.fromisoformat(date_str)\n            return make_string(vm, dt.strftime(fmt))\n        except:\n            return NullValue()\n    registry.register("date::format", fn_date_format)')
])

update_file("math_lib.py", [
    ('registry.register("math::ceil", fn_ceil)', 'registry.register("math::ceil", fn_ceil)\n    \n    def fn_sin(args, vm):\n        if not args: return NullValue()\n        return NumberValue(math.sin(args[0].to_python()))\n    registry.register("math::sin", fn_sin)\n    \n    def fn_cos(args, vm):\n        if not args: return NullValue()\n        return NumberValue(math.cos(args[0].to_python()))\n    registry.register("math::cos", fn_cos)\n    \n    def fn_log(args, vm):\n        if not args: return NullValue()\n        return NumberValue(math.log(args[0].to_python()))\n    registry.register("math::log", fn_log)\n    \n    def fn_random(args, vm):\n        return NumberValue(random.random())\n    registry.register("math::random", fn_random)')
])

print("Finished updates.")
