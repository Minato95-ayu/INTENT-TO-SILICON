
path = "D:/intent-to-silicon-research/INTENT-TO-SILICON/compiler/parser/parser.py"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

import re
new_list = "[\"container\", \"card\", \"row\", \"column\", \"page\", \"list\", \"grid\", \"stack\", \"center\", \"expanded\", \"padding\", \"scrollview\", \"appbar\", \"navigationbar\", \"drawer\", \"dialog\", \"snackbar\", \"form\"]"
c = re.sub(r"\[\"container\"[^\]]+\]", new_list, c)

with open(path, "w", encoding="utf-8") as f:
    f.write(c)

