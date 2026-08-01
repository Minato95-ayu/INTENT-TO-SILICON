
cli_path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/tools/cli.py"
with open(cli_path, "r", encoding="utf-8") as f:
    content = f.read()

old_code = """        renderer_cls = RENDERERS.get(args.renderer)
        renderer = renderer_cls(vm.event_queue)
        
        print(f"\\n--- Running AAYU App: {args.file} ---")"""

new_code = """        renderer_cls = RENDERERS.get(args.renderer)
        renderer = renderer_cls(vm.event_queue)
        if hasattr(renderer, "initialize"):
            renderer.initialize()
        
        print(f"\\n--- Running AAYU App: {args.file} ---")"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open(cli_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched cli.py")
else:
    print("Could not find old code in cli.py")

