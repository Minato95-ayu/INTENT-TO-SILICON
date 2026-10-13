# ==============================================================================
# AAYU Automated Handbook Snippet Verifier
# Runs all handbook code examples against the live 'aayu' toolchain
# ==============================================================================

$ErrorActionPreference = "Stop"

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "      AAYU HANDBOOK AUTOMATED SNIPPET RUNNER      " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$test_file = "$PSScriptRoot\handbook_temp_test.ay"

$snippets = @(
    @{ Name = "Hello World"; Code = "print(`"Hello, World!`")" },
    @{ Name = "Variables & State"; Code = "let lang = `"AAYU`"`nstate count = 1`nglobal SYS = `"IntentEngine`"`nprint(lang, count, SYS)" },
    @{ Name = "Arithmetic & Logic"; Code = "let a = 15`nlet b = 8`nprint(`"Area:`", a * b)`nprint(`"Even:`", (a * b) % 2 == 0)" },
    @{ Name = "Conditionals (if/elif/else)"; Code = "let m = 82`nif m >= 90`nprint(`"A+`")`nelif m >= 75`nprint(`"A`")`nelse`nprint(`"B`")`nend" },
    @{ Name = "While Loop Iteration"; Code = "let i = 1`nlet sum = 0`nwhile i <= 5`nsum = sum + i`ni = i + 1`nend`nprint(`"Sum:`", sum)" },
    @{ Name = "Functions (action)"; Code = "action add(x, y)`nreturn x + y`nend`nprint(`"Add:`", add(25, 75))" },
    @{ Name = "Arrays & Length"; Code = "let arr = [10, 20, 30]`nprint(`"Len:`", len(arr))`nprint(`"Item 1:`", arr[0])" },
    @{ Name = "Array Merge (+)"; Code = "let m = [1, 2] + [3, 4]`nprint(`"Merged:`", len(m))" },
    @{ Name = "Dictionaries"; Code = "let user = {`"name`": `"Ayush`", `"role`": `"Architect`"}`nprint(`"User:`", user[`"name`"])" },
    @{ Name = "std/math Sqrt & Pow"; Code = "import `"std/math`"`nprint(`"Sqrt:`", sqrt(64.0))`nprint(`"Pow:`", pow(2.0, 4.0))" },
    @{ Name = "std/crypto Hash Entropy"; Code = "import `"std/crypto`"`nlet h1 = hash_string(`"abc`")`nlet h2 = hash_string(`"xyz`")`nprint(`"Diff:`", h1 != h2)" },
    @{ Name = "std/db Record Store"; Code = "import `"std/db`"`nlet r = db_create_record(1, `"Task`", `"Active`")`nprint(`"ID:`", r[`"id`"])" }
)

$passed = 0
$failed = 0

foreach ($s in $snippets) {
    Set-Content -Path $test_file -Value $s.Code
    try {
        $out = & aayu $test_file 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host " [PASS] $($s.Name)" -ForegroundColor Green
            $passed++
        } else {
            Write-Host " [FAIL] $($s.Name): $out" -ForegroundColor Red
            $failed++
        }
    } catch {
        Write-Host " [FAIL] $($s.Name): $_" -ForegroundColor Red
        $failed++
    }
}

Remove-Item -Force $test_file, "$test_file.tmp.ayc" -ErrorAction SilentlyContinue

Write-Host "--------------------------------------------------" -ForegroundColor Cyan
$res_color = "Green"
if ($failed -gt 0) { $res_color = "Red" }
Write-Host "Results: $passed Passed | $failed Failed" -ForegroundColor $res_color
Write-Host "==================================================" -ForegroundColor Cyan

if ($failed -gt 0) { exit 1 }
