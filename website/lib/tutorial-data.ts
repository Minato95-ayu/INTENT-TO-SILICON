import { ChapterData } from "./tutorial-types";

// Every program used in this course is a checked-in regression example. The
// test harness verifies both successful execution and its expected output.
const testPath = "https://github.com/Minato95-ayu/INTENT-TO-SILICON/blob/main/tests/";

export const chapters: ChapterData[] = [
  {
    slug: "chapter-1", num: 1, title: "Values, variables, and text", phase: "AAYU Core - Verified",
    description: "Start with bindings, integer literals, strings, and string concatenation.",
    learningPoints: ["Declare values with let", "Read a bound value", "Join strings with +", "Run and inspect a checked example"],
    content: `## The smallest useful program\n\nAAYU source files use the '.aayu' extension. The [checked example](${testPath}test_01_vars.aayu) declares string and integer values, prints each one, and joins two strings.\n\n\`\`\`aayu\nlet name = "AAYU"\nlet major = 1\nlet greeting = "Hello from " + name\nprint(greeting)\n\`\`\`\n\nThis is a shortened excerpt from the checked regression program. The full example also prints the minor and patch version values.\n\n## Run it\n\nFrom the repository root on Windows, run **bin/aayu-vm tests/test_01_vars.aayu**. On Linux or macOS, build and install both tools as described in the installation guide, then run **aayu-vm tests/test_01_vars.aayu**; the compiler must be available beside the VM.\n\nExpected final line: 'Hello from AAYU'. The project test harness checks the full output.`,
    exercise: "Copy the checked example to hello.aayu. Change the name and greeting, then run it. Compare your output with the source-level changes you made."
  },
  {
    slug: "chapter-2", num: 2, title: "Numbers and arithmetic", phase: "AAYU Core - Verified",
    description: "Use integer and floating point literals with addition, subtraction, multiplication, and division.",
    learningPoints: ["Write integer and decimal literals", "Combine arithmetic operators", "Store an expression in a variable", "Check numeric output"],
    content: `## Arithmetic expressions\n\nThe [checked numeric example](${testPath}test_02_floats.aayu) exercises decimal literals, multiplication, division, and subtraction.\n\n\`\`\`aayu\nlet pi = 3.14159\nlet radius = 10.0\nlet area = pi * radius * radius\nprint(area)\n\`\`\`\n\nMultiplication is evaluated before addition/subtraction. The complete test also prints '180.0 / 2.0' and '180.0 - 30.0'; its expected values are 314.159, 90, and 150.\n\nRun 'bin/aayu-vm tests/test_02_floats.aayu'.`,
    exercise: "Change the radius to 2.0. Work out the expected area first, run the program, and compare. Then change one operator and explain the difference."
  },
  {
    slug: "chapter-3", num: 3, title: "While loops and accumulators", phase: "AAYU Core - Verified",
    description: "Repeat a block with while and build a running total through assignment.",
    learningPoints: ["Initialize loop state", "Write a while condition", "Update a variable each iteration", "Check a known sum"],
    content: `## Count and accumulate\n\nThe [loop regression example](${testPath}test_03_loops.aayu) adds the numbers 0 through 9. It starts both variables at zero, then increments 'count' until the condition is false.\n\n\`\`\`aayu\nlet count = 0\nlet sum = 0\nwhile count < 10\n    sum = sum + count\n    count = count + 1\nend\nprint(sum)\n\`\`\`\n\nExpected sum: 45. If the counter update is removed, the loop never ends; if the condition changes to 'count < 9', the final sum changes. The regression file also checks the result with an if/else.`,
    exercise: "Change the condition to count < 5. Predict the sum, run the program, and explain why the last included value is 4."
  },
  {
    slug: "chapter-4", num: 4, title: "Conditions and branches", phase: "AAYU Core - Verified",
    description: "Use if/else to check a computed result and print the matching branch.",
    learningPoints: ["Compare values with ==", "Choose a branch with if/else", "Use conditions to validate a result", "Keep failure output visible"],
    content: `## Make a result check itself\n\nThe loop regression checks whether its computed sum is 45. The [combined verification example](${testPath}test_suite_proof.aayu) also checks a Fibonacci result with an if/else branch.\n\n\`\`\`aayu\nif a == 6765\n    print("TEST PASSED: Fibonacci matches 6765!")\nelse\n    print("TEST FAILED")\nend\n\`\`\`\n\nA program exiting successfully does not prove its answer is right. This explicit branch makes a wrong result visible; the test runner also compares complete expected output.`,
    exercise: "Change 6765 to 6764. Run the program and confirm the failure branch is printed. Restore the correct value afterward."
  },
  {
    slug: "chapter-5", num: 5, title: "Build Fibonacci with a loop", phase: "AAYU Core - Verified",
    description: "Combine bindings, arithmetic, a loop, and a result check in a small complete program.",
    learningPoints: ["Track two previous values", "Compute the next value", "Repeat a fixed number of times", "Verify Fibonacci(20) equals 6765"],
    content: `## A complete core-language exercise\n\nThe [Fibonacci regression program](${testPath}test_04_fibonacci.aayu) computes the sequence iteratively. It keeps the two latest values in 'a' and 'b', computes their sum, shifts the pair, and repeats 20 times.\n\n\`\`\`aayu\nlet a = 0\nlet b = 1\nlet i = 0\nwhile i < 20\n    let temp = a + b\n    a = b\n    b = temp\n    i = i + 1\nend\nprint(a)\n\`\`\`\n\nExpected result: 6765. This version uses a loop and does not demonstrate recursive function calls. The separate regression example checks the result in an if/else.`,
    exercise: "Change the loop bound to 10. The printed value should be 55. Add an if/else check for 55 and run the regression harness."
  },
  {
    slug: "chapter-6", num: 6, title: "Run the checks and read the limits", phase: "Tooling - Verified",
    description: "Run the project's regression/security checks and learn what those checks do and do not establish.",
    learningPoints: ["Run the PowerShell test harness", "Read expected-output failures", "Distinguish core tests from feature support", "Consult the known limitations list"],
    content: `## Verify the examples\n\nFrom the repository root on Windows, run:\n\n\`\`\`powershell\npowershell -ExecutionPolicy Bypass -File tests/run_tests.ps1\n\`\`\`\n\nThe harness compiles and runs the checked AAYU regression programs, checks their outputs, and runs malformed-bytecode checks for the VM and JIT.\n\nA passing result only applies to the covered tests. It does not verify the old course chapters about HTTP servers, SQL, UI applications, AI/ML, package registries, or deployment. Check the repository's 'KNOWN_LIMITATIONS.md' before relying on those areas.`,
    exercise: "Intentionally change the expected output for one regression example in the test harness. Run it, inspect the failure, then restore the correct expectation."
  }
];
