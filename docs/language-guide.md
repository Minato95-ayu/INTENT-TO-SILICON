# AAYU Language Guide

This guide replaces an older draft whose period-terminated `entity` and `fn` examples are not accepted by the current compiler. The verified starter syntax is:

```aayu
let x = 10
let y = 20
let total = x + y

if total == 30
    print("total: 30")
else
    print("unexpected total")
end
```

See the [implementation-aligned language reference](language_reference.md) and [core regression examples](../tests/). Basic user-defined actions are now supported; module imports and package resolution are not implemented by the current compiler/VM.
