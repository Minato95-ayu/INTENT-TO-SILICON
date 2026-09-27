with open("tools/commands/run.py", "r") as f:
    text = f.read()

target = """        if not renderer:
            # Headless mode, no UI to render, skip frame loop
            pass
        else:"""

replacement = """        if not renderer:
            # Headless mode, no UI to render, skip frame loop
            if "main" in vm.action_addresses:
                vm.call_action_by_name("main")
                vm.execute()
        else:"""

if target in text:
    with open("tools/commands/run.py", "w") as f:
        f.write(text.replace(target, replacement))
    print("Fixed headless mode!")
else:
    print("Target not found")