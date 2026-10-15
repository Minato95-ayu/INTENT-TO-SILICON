import Link from 'next/link';
import { Package, CheckCircle2, Terminal, Code2, Cpu } from 'lucide-react';

interface StdModule {
  name: string;
  category: string;
  description: string;
  functions: string[];
  example: string;
}

const standardModules: StdModule[] = [
  {
    name: 'std/collections',
    category: 'Data Structures & Algorithms',
    description: 'Dynamic arrays, selection sort, string tokenization, functional predicates, and zero-boilerplate number parsing.',
    functions: ['sorted(arr)', 'split(str, delim)', 'strip(str)', 'replace(str, a, b)', 'lower(str)', 'upper(str)', 'parse_ints(arr)', 'sum(arr)', 'mean(arr)', 'enumerate(arr)', 'any(arr)', 'all(arr)', 'zip(a, b)', 'contains(arr, val)'],
    example: 'import "std/collections"\nlet s = sorted([50, 10, 40])\nlet money = parse_ints(split("10 20 30", " "))\nprint("Total: " + sum(money))'
  },
  {
    name: 'std/math',
    category: 'Mathematics & Neural Activations',
    description: 'Hardware-level arithmetic, square roots via Newton-Raphson approximation, power exponentiation, and neural activations.',
    functions: ['sqrt(x)', 'abs(x)', 'pow(base, exp)', 'max(a, b)', 'min(a, b)', 'clamp(val, low, high)', 'relu(x)', 'sigmoid(x)'],
    example: 'import "std/math"\nlet root = sqrt(49.0)\nlet bound = clamp(root * 2.5, 0.0, 10.0)\nprint("Bounded root: " + bound)'
  },
  {
    name: 'std/brain',
    category: 'AAYU BrainOS AI Guard',
    description: 'Autonomous AI coding guard, anti-hallucination syntax checking, context handoff snapshotting, and architectural freeze protection.',
    functions: ['brain_anti_hallucinate(code)', 'brain_context_handoff(snapshot)', 'brain_security_guard(code)', 'brain_is_frozen(module)', 'brain_ai_guidance()'],
    example: 'import "std/brain"\nlet check = brain_is_frozen("Lexer")\nlet report = brain_security_guard(apiKeySnippet)\nprint("Is Frozen: " + check)'
  },
  {
    name: 'std/os',
    category: 'Operating System Primitives',
    description: 'Native host platform discovery, CPU architecture querying, process signals, and type inspection.',
    functions: ['get_os()', 'get_architecture()', 'get_env_var(name)', 'get_type(value)'],
    example: 'import "std/os"\nprint("Platform: " + get_os())\nprint("Architecture: " + get_architecture())'
  },
  {
    name: 'std/fs',
    category: 'File System & Paths',
    description: 'File reading and writing, path manipulation, extension parsing, and existence checking.',
    functions: ['read_text(path)', 'write_text(path, content)', 'file_exists(path)', 'format_path(dir, file)', 'get_extension(path)'],
    example: 'import "std/fs"\nlet p = format_path("data", "app.ay")\nlet ext = get_extension("archive.tar.gz")\nprint("Path: " + p + " (" + ext + ")")'
  },
  {
    name: 'std/crypto',
    category: 'Cryptographic Hashing & Merkle Trees',
    description: 'Pure AAYU dual-polynomial polynomial cryptographic hashing, accumulator digests, and Merkle tree root computations.',
    functions: ['hash_string(data)', 'merkle_root(leaf_hashes)', 'get_char_byte(ch)'],
    example: 'import "std/crypto"\nlet digest = hash_string("INTENT-TO-SILICON")\nprint("SHA-equivalent Digest: " + digest)'
  },
  {
    name: 'std/json',
    category: 'Serialization Engine',
    description: 'RFC 8259 compliant JSON stringify, quotation escaping, and key-value pair formatting without external packages.',
    functions: ['json_quote(s)', 'json_format_pair(k, v)', 'json_format_object(pairs)', 'json_format_array(items)'],
    example: 'import "std/json"\nlet pair = json_format_pair("version", json_quote("1.2.0"))\nprint(pair)'
  },
  {
    name: 'std/db',
    category: 'Embedded Record Store',
    description: 'In-memory relational record store, primary key lookups, and dynamic multi-attribute query filtering.',
    functions: ['db_create_record(id, name, val)', 'db_filter_records(recs, field, val)', 'db_find_by_id(recs, id)', 'db_count_records(recs)'],
    example: 'import "std/db"\nlet r1 = db_create_record(1, "Post", 100)\nlet found = db_find_by_id([r1], 1)\nprint("Found: " + found["name"])'
  },
  {
    name: 'std/ai',
    category: 'Machine Learning & Tensors',
    description: 'Vector arithmetic, matrix-vector multiplication, multi-layer perceptron (MLP) forward passes, and anomaly scoring.',
    functions: ['vec_add(v1, v2)', 'mat_vec_mul(matrix, vec)', 'mlp_forward_pass(features)', 'detect_anomaly(score, threshold)'],
    example: 'import "std/ai"\nlet res = vec_add([1.0, 2.0], [10.0, 20.0])\nprint("Result: [" + res[0] + ", " + res[1] + "]")'
  },
  {
    name: 'std/ui',
    category: 'Declarative Reactive UI',
    description: 'Widget-tree primitives (Column, Row, Text, Button, Card) rendering directly into clean zero-dependency HTML/CSS.',
    functions: ['create_text(content)', 'create_button(label, action)', 'create_column(children)', 'create_row(children)', 'render(tree)'],
    example: 'import "std/ui"\nlet tree = create_column([create_text("AAYU"), create_button("Run", "start")])\nlet html = render(tree)\nprint(html)'
  },
  {
    name: 'std/ledger',
    category: 'Consensus & Audit Log',
    description: 'Immutable transaction state transitions, UTXO balance verification, and invariant rule assertion.',
    functions: ['verify_balance(bal, amt, fee)', 'apply_transfer(from, to, amt)', 'verify_chain_link(prev, cur)', 'verify_intent_invariant(...)'],
    example: 'import "std/ledger"\nlet ok = verify_balance(500, 100, 5)\nlet next = apply_transfer(500, 200, 100)\nprint("Sender Bal: " + next[0])'
  },
  {
    name: 'std/ayon',
    category: 'AAYU Object Notation Wire Protocol',
    description: 'Human-readable, comment-aware serialization protocol with automatic comment stripping and dictionary bridging.',
    functions: ['ayon_strip_comments(src)', 'ayon_is_space(c)'],
    example: 'import "std/ayon"\nlet clean = ayon_strip_comments("# Note\\nkey: \\"value\\"")\nprint(clean)'
  },
  {
    name: 'std/http',
    category: 'HTTP Client & Request Protocol',
    description: 'HTTP protocol parsing, URL scheme extraction, standard status code validators, and wire payload formatting.',
    functions: ['parse_url_protocol(url)', 'format_request(method, path, host, body)', 'status_is_ok(status_code)'],
    example: 'import "std/http"\nlet proto = parse_url_protocol("https://aayu.dev")\nprint("Protocol: " + proto + " | OK: " + status_is_ok(200))'
  },
  {
    name: 'std/server',
    category: 'ASGI Web Server & Response Builders',
    description: 'HTTP response builders, MIME content-type headers, and JSON/HTML response formatters.',
    functions: ['format_response(status, type, body)', 'json_response(status, data)', 'html_response(status, html)'],
    example: 'import "std/server"\nlet resp = json_response(200, "{\\"status\\":\\"ready\\"}")\nprint(resp)'
  },
  {
    name: 'std/test',
    category: 'Native Unit Testing & Assertions',
    description: 'Zero-dependency assertion engine, test suite coordinator, and test runner with granular value and type-coerced validation.',
    functions: ['assert_eq(actual, exp, name)', 'assert_neq(actual, unexp, name)', 'assert_true(cond, name)', 'assert_false(cond, name)', 'assert_gt(a, b, name)', 'assert_lt(a, b, name)', 'test_begin_suite(name)', 'test_end_suite()'],
    example: 'import "std/test"\ntest_begin_suite("Math Suite")\nassert_eq(sqrt(81.0), 9.0, "Root check")\ntest_end_suite()'
  },
  {
    name: 'std/contracts',
    category: 'Intent-to-Silicon Contracts',
    description: 'Design-by-Contract verification primitives for mission-critical intent enforcement, type checking, and system invariants.',
    functions: ['require(cond, name)', 'ensure(cond, name)', 'invariant(cond, name)', 'check_type(val, exp_type, param)'],
    example: 'import "std/contracts"\naction withdraw(bal, amt)\n  require(amt > 0, "positive amount")\n  return bal - amt\nend'
  }
];

export default function PackagesPage() {
  return (
    <main className="min-h-screen bg-[#050505] text-white pt-28 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-semibold mb-4">
            <CheckCircle2 className="w-4 h-4" /> 100% Pure Self-Hosted Standard Library (Zero Python, Zero C)
          </div>
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            AAYU Standard Libraries (All 16 Production Modules)
          </h1>
          <p className="text-lg text-zinc-400 max-w-3xl mx-auto">
            Production-ready, deterministic standard libraries running natively on the AAYU Silicon Stack VM.
            Every module is importable with standard <code className="text-purple-400">import &quot;std/&lt;name&gt;&quot;</code> syntax.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-16">
          {standardModules.map((mod) => (
            <div
              key={mod.name}
              className="bg-[#0a0a0c] border border-white/10 rounded-2xl p-6 flex flex-col justify-between hover:border-cyan-500/40 transition-all duration-200"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-lg font-bold text-cyan-300">{mod.name}</span>
                  <span className="text-xs px-2.5 py-1 rounded-full bg-white/5 border border-white/10 text-zinc-400 font-medium">
                    {mod.category}
                  </span>
                </div>
                <p className="text-sm text-zinc-300 mb-4 leading-relaxed">{mod.description}</p>
                
                <div className="mb-4">
                  <div className="text-xs uppercase tracking-wider text-zinc-500 font-semibold mb-2">Key Exported Actions</div>
                  <div className="flex flex-wrap gap-1.5">
                    {mod.functions.map((fn) => (
                      <span key={fn} className="font-mono text-xs px-2 py-0.5 rounded bg-white/5 border border-white/10 text-purple-300">
                        {fn}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div>
                <div className="text-xs uppercase tracking-wider text-zinc-500 font-semibold mb-1">Example Usage</div>
                <pre className="bg-black/60 border border-white/5 rounded-xl p-3 font-mono text-xs text-emerald-400 overflow-x-auto">
                  <code>{mod.example}</code>
                </pre>
              </div>
            </div>
          ))}
        </div>

        <div className="bg-[#0a0a0c] border border-white/10 rounded-2xl p-8 text-center max-w-3xl mx-auto">
          <Cpu className="w-10 h-10 text-cyan-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">Deterministic Execution on Native Silicon</h2>
          <p className="text-sm text-zinc-400 mb-6">
            All 14 standard libraries compile directly to compact bytecode and execute on the Rust Silicon Stack VM with zero external runtime dependencies.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/docs"
              className="px-6 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-sm transition"
            >
              Read Full Documentation
            </Link>
            <Link
              href="/downloads/aayu-android.apk"
              className="px-6 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium text-sm transition"
            >
              Download Mobile IDE APK
            </Link>
          </div>
        </div>
      </div>
    </main>
  );
}
