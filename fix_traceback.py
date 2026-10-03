import sys

def patch():
    with open("tools/commands/run.py", "r", encoding="utf-8") as f:
        content = f.read()

    target = """    except Exception as e:
        print(f"\\nRuntime Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)"""
        
    new_target = """    except Exception as e:
        from runtime.vm.exceptions import AayuException
        if isinstance(e, AayuException):
            print(f"\\n[AAYU PANIC] {e.exc_type}: {e.message}")
            if hasattr(e, 'stacktrace') and e.stacktrace:
                print("--- AAYU Stack Trace ---")
                for frame in e.stacktrace:
                    print(f"  at {frame}")
        else:
            print(f"\\n[AAYU INTERNAL ERROR] Something went wrong in the AAYU engine.")
            print(f"Error: {str(e)}")
        sys.exit(1)"""

    if target in content:
        content = content.replace(target, new_target)
        with open("tools/commands/run.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("Patched run.py!")
    else:
        print("Target not found in run.py")

patch()
