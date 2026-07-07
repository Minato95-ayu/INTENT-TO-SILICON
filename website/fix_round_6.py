import os
import re

repo = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website'

def replace_exact(path_suffix, old, new):
    path = os.path.join(repo, path_suffix)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            t = f.read()
        if type(old) is str:
            t = t.replace(old, new)
        else:
            t = re.sub(old, new, t)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(t)

# 1. app/brainos/page.tsx
replace_exact('app/brainos/page.tsx', re.compile(r'\{\[BrainOS Decision Engine\][^}]*\}', re.DOTALL), r'[BrainOS Decision Engine]\nAnalyzing requirements for: "Scalable Banking Core"\n\nConstraints Detected:\n- Requires ACID compliance\n- Needs sub-10ms latency\n\nTradeoff Analysis:\n1. PostgreSQL (ACID ✅, Latency ⚠️)\n2. Redis + Postgres (ACID ✅, Latency ✅)\n\nRecommendation: Redis + PostgreSQL')
# Wait, replacing everything between { and } might be too greedy. Let's just do a specific string replace:
path_b = os.path.join(repo, 'app/brainos/page.tsx')
with open(path_b, 'r', encoding='utf-8') as f:
    tb = f.read()
tb = tb.replace('{[BrainOS Decision Engine]\nAnalyzing requirements for: "Scalable Banking Core"\n\nConstraints Detected:\n- Requires ACID compliance\n- Needs sub-10ms latency\n\nTradeoff Analysis:\n1. PostgreSQL (ACID ✅, Latency ⚠️)\n2. Redis + Postgres (ACID ✅, Latency ✅)\n\nRecommendation: Redis + PostgreSQL}', '{[BrainOS Decision Engine]\nAnalyzing requirements for: "Scalable Banking Core"\n\nConstraints Detected:\n- Requires ACID compliance\n- Needs sub-10ms latency\n\nTradeoff Analysis:\n1. PostgreSQL (ACID ✅, Latency ⚠️)\n2. Redis + Postgres (ACID ✅, Latency ✅)\n\nRecommendation: Redis + PostgreSQL}')
with open(path_b, 'w', encoding='utf-8') as f:
    f.write(tb)

# 2. data/language-content.tsx
path_l = os.path.join(repo, 'data/language-content.tsx')
with open(path_l, 'r', encoding='utf-8') as f:
    tl = f.read()
tl = re.sub(r'\{\s*fn main\(\) -> Void\ndo\n    print\("Hello, AAYU World!"\)\.\nend\.\}', '{n main() -> Void\\ndo\\n    print("Hello, AAYU World!").\\nend.}', tl)
# Sometimes it's corrupted as "\fn" or "n"
tl = re.sub(r'\{n main\(\).*?end\.\}', '{n main() -> Void\\ndo\\n    print("Hello, AAYU World!").\\nend.}', tl, flags=re.DOTALL)
with open(path_l, 'w', encoding='utf-8') as f:
    f.write(tl)

print("Fixed round 6")
