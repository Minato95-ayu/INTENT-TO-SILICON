"""Explicit Node.js ecosystem bindings for AAYU interop."""

import json
import shutil
import subprocess


class JavaScriptInteropError(RuntimeError):
    """Raised when a Node.js module function cannot be invoked."""


_NODE_SCRIPT = r"""
const fs = require('fs');
const request = JSON.parse(fs.readFileSync(0, 'utf8'));
let target = require(request.module);
for (const part of request.symbol.split('.')) target = target[part];
if (typeof target !== 'function') throw new Error('export is not callable');
const result = target(...request.args);
if (result && typeof result.then === 'function') {
  result.then(value => process.stdout.write(JSON.stringify(value ?? null)));
} else {
  process.stdout.write(JSON.stringify(result ?? null));
}
"""


def bind_javascript_function(vm, module: str, symbol: str, aayu_name: str) -> None:
    node = shutil.which("node")
    if not node:
        raise JavaScriptInteropError("Node.js is required for JavaScript library bindings")
    if not module or not symbol or any(part == "" for part in symbol.split(".")):
        raise JavaScriptInteropError("JavaScript bindings require a module and export name")

    def call(args, _vm):
        request = json.dumps({"module": module, "symbol": symbol, "args": args})
        result = subprocess.run(
            [node, "-e", _NODE_SCRIPT],
            input=request,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = result.stderr.strip() or "Node.js function failed"
            raise JavaScriptInteropError(detail)
        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise JavaScriptInteropError("Node.js function returned invalid JSON") from exc

    vm.stdlib.register_js_external(aayu_name, call)