with open("tools/commands/run.py", "r") as f:
    text = f.read()

target = """        if renderer_type == "console":
            renderer.shutdown()
            return"""

replacement = """        if renderer_type == "console":
            if "main" in vm.action_addresses:
                vm.call_action_by_name("main")
                vm.execute()
            renderer.shutdown()
            return"""

if target in text:
    with open("tools/commands/run.py", "w") as f:
        f.write(text.replace(target, replacement))
    print("Fixed run.py!")
else:
    print("Target not found in run.py")