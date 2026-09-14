with open("runtime/stdlib/modules/database_lib.py", "r") as f:
    content = f.read()

content = content.replace("except Exception:", "except Exception as e:\n            print(f'DB Error: {e}')")

with open("runtime/stdlib/modules/database_lib.py", "w") as f:
    f.write(content)
