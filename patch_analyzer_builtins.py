with open("compiler/semantic/analyzer.py", "r", encoding="utf-8") as f:
    content = f.read()

old_builtins = """            ("string::split", 2), ("string::trim", 1), ("string::replace", 3),
            ("string::upper", 1), ("string::lower", 1), ("string::contains", 2),
            ("string::starts_with", 2), ("string::ends_with", 2), ("string::length", 1)"""

new_builtins = """            ("string::split", 2), ("string::trim", 1), ("string::replace", 3),
            ("string::upper", 1), ("string::lower", 1), ("string::contains", 2),
            ("string::starts_with", 2), ("string::ends_with", 2), ("string::length", 1),
            ("string::substring", 3), ("string::char_at", 2), ("string::char_code", 2),
            ("list::push", 2), ("list::pop", 1), ("list::shift", 1), ("list::unshift", 2),
            ("list::length", 1), ("list::get", 2), ("list::set", 3), ("list::remove", 2),
            ("list::contains", 2), ("list::insert", 3), ("list::reverse", 1), ("list::sort", 1)"""

if old_builtins in content:
    content = content.replace(old_builtins, new_builtins)
    with open("compiler/semantic/analyzer.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Patched analyzer successfully.")
else:
    print("Could not find builtins block")
