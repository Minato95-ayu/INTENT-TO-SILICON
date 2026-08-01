
import re
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/semantic/nodes.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("@dataclass(frozen=True)", "@dataclass")

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

