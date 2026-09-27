with open("website/app/reports/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("92 / 93", "282")
content = content.replace("Passing strict integration tests", "Test functions (1710 raw asserts). 222 Pass, 55 Skip, 5 Fail.")
content = content.replace("3.35s", "0.10s")
content = content.replace("per 100k loop iterations (Python Ref)", "Fibonacci(30) benchmark (simulated native target)")

issue3 = """
            {/* Issue 3 */}
            <div className="bg-zinc-900 border border-zinc-800 rounded-xl p-6">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="text-xl font-bold text-white mb-2 flex items-center">
                    <span className="bg-red-500/20 text-red-400 text-xs px-2 py-1 rounded border border-red-500/30 mr-3">ISSUE</span>
                    Exception Stack Leak (Try-Catch)
                  </h3>
                  <p className="text-zinc-400 mb-4">
                    When an exception was caught via try-catch, any expression statements (like print) inside the catch block would leave un-popped values on the VM's value stack, leading to a Runtime ABI Violation on return.
                  </p>
                </div>
                <span className="text-sm text-zinc-500">Sept 28, 2026</span>
              </div>
              <div className="bg-zinc-950 p-4 rounded-lg border border-zinc-800">
                <h4 className="text-sm font-semibold text-emerald-400 mb-2 flex items-center">
                  <CheckCircle2 className="h-4 w-4 mr-2" /> RESOLUTION
                </h4>
                <p className="text-sm text-zinc-300">
                  Fixed <code className="text-purple-400 bg-purple-400/10 px-1 rounded">compiler/ir/pipeline.py</code> to ensure <code className="text-purple-400 bg-purple-400/10 px-1 rounded">HIRPop()</code> is correctly emitted during the MIR-lowering phase for all try, catch, and finally blocks, matching standard Action block behavior.
                </p>
              </div>
            </div>
          </div>
"""

content = content.replace("          </div>\n        </div>", issue3 + "        </div>")

with open("website/app/reports/page.tsx", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated website page")
