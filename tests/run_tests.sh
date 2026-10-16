#!/usr/bin/env bash
set -e

echo "=================================================="
echo "       AAYU INTENT-TO-SILICON TEST RUNNER (LINUX) "
echo "=================================================="

BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../bin" && pwd)"
BIN_AAYUC="$BIN_DIR/aayuc"
BIN_VM="$BIN_DIR/aayu-vm"
if [ ! -f "$BIN_VM" ]; then
    BIN_VM="$BIN_DIR/aayu"
fi

if [ ! -f "$BIN_AAYUC" ] || [ ! -f "$BIN_VM" ]; then
    echo "[ERROR] Compiler ($BIN_AAYUC) or VM ($BIN_VM) not found in bin/"
    exit 1
fi

chmod +x "$BIN_AAYUC" "$BIN_VM"

TEST_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PASSED=0
FAILED=0

for file in "$TEST_DIR"/*.aayu; do
    [ -e "$file" ] || continue
    base=$(basename "$file" .aayu)
    if [ "$base" = "test_lint_target" ]; then
        continue
    fi
    ayc="$TEST_DIR/$base.ayc"
    
    printf "[TEST] Running %s... " "$base.aayu"
    
    # 1. Compile
    if ! "$BIN_AAYUC" "$file" -o "$ayc" > /dev/null 2>&1; then
        echo "FAIL (Compilation)"
        FAILED=$((FAILED + 1))
        continue
    fi
    
    # 2. Execute
    if "$BIN_VM" "$ayc" > /dev/null 2>&1; then
        echo "PASS"
        PASSED=$((PASSED + 1))
    else
        echo "FAIL (Runtime error)"
        FAILED=$((FAILED + 1))
    fi
    
    rm -f "$ayc"
done

# Run Static Linter Verification
if [ -f "$TEST_DIR/test_lint_target.aayu" ]; then
    printf "[TEST] Running Static Linter on test_lint_target.aayu... "
    if "$BIN_VM" lint "$TEST_DIR/test_lint_target.aayu" 2>&1 | grep -q "deprecated keyword 'var'"; then
        echo "PASS"
        PASSED=$((PASSED + 1))
    else
        echo "FAIL (Linter did not detect deprecated var)"
        FAILED=$((FAILED + 1))
    fi
fi

echo "--------------------------------------------------"
echo "Results: $PASSED Passed | $FAILED Failed"
echo "=================================================="

if [ "$FAILED" -gt 0 ]; then
    exit 1
fi
exit 0
