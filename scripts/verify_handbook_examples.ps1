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
    @{ Name = "std/db Record Store"; Code = "import `"std/db`"`nlet r = db_create_record(1, `"Task`", `"Active`")`nprint(`"ID:`", r[`"id`"])" },
    @{ Name = "DSA: Binary Search"; Code = "action bs(arr, t)`nlet l = 0`nlet h = len(arr)-1`nwhile l <= h`nlet m = (l+h)/2`nif arr[m] == t`nreturn m`nelif arr[m] < t`nl = m + 1`nelse`nh = m - 1`nend`nend`nreturn -1`nend`nprint(`"BS:`", bs([10, 20, 30, 40], 30))" },
    @{ Name = "DSA: Bubble Sort & SetAt"; Code = "action set_at(arr, idx, val)`nlet res = []`nlet i = 0`nwhile i < len(arr)`nif i == idx`nres = res + [val]`nelse`nres = res + [arr[i]]`nend`ni = i + 1`nend`nreturn res`nend`nlet a = [3, 1, 2]`na = set_at(a, 0, 1)`nprint(`"SetAt:`", a[0])" },
    @{ Name = "DSA: Stack LIFO"; Code = "action spush(s, v)`nreturn s + [v]`nend`nlet s = spush([], 42)`nprint(`"Stack:`", s[0])" },
    @{ Name = "Project: Base62 URL Shortener"; Code = "action b62(n)`nlet c = `"0123456789abcdefghijklmnopqrstuvwxyz`"`nlet s = `"`"`nwhile n > 0`ns = c[n % 36] + s`nn = n / 36`nend`nreturn s`nend`nprint(`"B62:`", b62(100))" },
    @{ Name = "Logic: Missing Number in 1..N"; Code = "action miss(a, n)`nlet exp = (n * (n + 1)) / 2`nlet act = 0`nlet i = 0`nwhile i < len(a)`nact = act + a[i]`ni = i + 1`nend`nreturn exp - act`nend`nprint(`"Missing:`", miss([1, 2, 4, 5], 5))" },
    @{ Name = "Logic: Palindrome Two Pointers"; Code = "action pal(s)`nlet l = 0`nlet r = len(s) - 1`nwhile l < r`nif s[l] != s[r]`nreturn 0`nend`nl = l + 1`nr = r - 1`nend`nreturn 1`nend`nprint(`"Pal:`", pal(`"racecar`"))" }
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
