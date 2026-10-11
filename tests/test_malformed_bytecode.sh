#!/usr/bin/env bash
# Malformed Bytecode Security Verification Suite (Linux / POSIX)
# Tests rejection of corrupt bytecode with non-zero exit codes in both Interpreter and JIT modes

set -euo pipefail

echo "=================================================="
echo "     AAYU BYTECODE VERIFIER & SECURITY TEST (SH)  "
echo "=================================================="

VM="./bin/aayu"
if [ ! -f "$VM" ]; then
    VM="./runtime_rs/target/release/aayu-vm"
fi
if [ ! -f "$VM" ]; then
    VM="./bin/aayu-vm"
fi

if [ ! -f "$VM" ]; then
    echo "[ERROR] VM executable not found!"
    exit 1
fi
chmod +x "$VM" 2>/dev/null || true

TEMP_DIR=$(mktemp -d /tmp/aayu_malformed_XXXXXX)
trap 'rm -rf "$TEMP_DIR"' EXIT

passed=0
failed=0

run_case() {
    local name="$1"
    local hex_data="$2"
    local expected="$3"

    local file_path="$TEMP_DIR/test.ayc"
    if [ -z "$hex_data" ]; then
        : > "$file_path"
    else
        printf '%b' "$hex_data" > "$file_path"
    fi

    # 1. Test Interpreter Mode
    local code_interp=0
    local out_interp
    set +e
    out_interp=$("$VM" run "$file_path" 2>&1)
    code_interp=$?
    set -e

    local interp_ok=0
    if [ "$code_interp" -ne 0 ] && echo "$out_interp" | grep -qi "$expected"; then
        interp_ok=1
    fi

    # 2. Test JIT Mode (Verifier must NOT be bypassed)
    local code_jit=0
    local out_jit
    set +e
    out_jit=$("$VM" run "$file_path" --jit 2>&1)
    code_jit=$?
    set -e

    local jit_ok=0
    if [ "$code_jit" -ne 0 ] && echo "$out_jit" | grep -qi "$expected"; then
        jit_ok=1
    fi

    if [ "$interp_ok" -eq 1 ] && [ "$jit_ok" -eq 1 ]; then
        echo " [PASS] $name safely rejected on both Interpreter & JIT (Code: $code_interp/$code_jit)"
        passed=$((passed + 1))
    else
        echo " [FAIL] $name rejection failed:"
        if [ "$interp_ok" -ne 1 ]; then
            echo "   Interpreter failed: Code=$code_interp, Output=$out_interp"
        fi
        if [ "$jit_ok" -ne 1 ]; then
            echo "   JIT failed: Code=$code_jit, Output=$out_jit"
        fi
        failed=$((failed + 1))
    fi
}

# Case 1: Empty file
run_case "Empty file" "" "missing magic header"

# Case 2: Invalid magic header (BAD!)
run_case "Invalid magic header" '\x42\x41\x44\x21\x00\x00\x00\x00' "Invalid magic header"

# Case 3: Truncated string table
run_case "Truncated string table" '\x41\x41\x59\x55\x05\x00\x00\x00' "Truncated bytecode"

# Case 4: Illegal opcode (0xEE)
run_case "Illegal opcode (0xEE)" '\x41\x41\x59\x55\x00\x00\x00\x00\x00\x00\x00\x00\xEE' "illegal opcode 0xEE"

# Case 5: Out-of-bounds jump target
run_case "Out-of-bounds jump target" '\x41\x41\x59\x55\x00\x00\x00\x00\x00\x00\x00\x00\x20\xFF\x00' "exceeds bytecode bounds"

# Case 6: Truncated PUSH_CONST operand
run_case "Truncated PUSH_CONST operand" '\x41\x41\x59\x55\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00' "Truncated operand for PUSH_CONST"

# Case 7: Misaligned jump target
run_case "Misaligned jump target into instruction operand" '\x41\x41\x59\x55\x00\x00\x00\x00\x01\x00\x00\x00\x01\x2A\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x20\x00\x01' "instruction boundary"

# Case 8: Stack underflow via Pass 3 abstract verifier
run_case "Stack underflow (POP on empty stack)" '\x41\x41\x59\x55\x00\x00\x00\x00\x00\x00\x00\x00\x02' "Stack underflow"

echo "--------------------------------------------------"
echo "Security Results: $passed Passed | $failed Failed"
echo "=================================================="

if [ "$failed" -gt 0 ]; then
    exit 1
else
    exit 0
fi
