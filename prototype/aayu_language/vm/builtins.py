def builtin_print(vm, args):
    text = " ".join(map(str, args))
    print(text)
    vm.output.append(text)
    return None

def builtin_len(vm, args):
    if not args:
        return 0
    return len(args[0])

BUILTINS = {
    "print": builtin_print,
    "len": builtin_len,
}
