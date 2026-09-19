# ==============================================================================
# COPYRIGHT (C) 2026 AYUSH GHRIT KAUSHIK. ALL RIGHTS RESERVED.
# 
# This source code is the proprietary intellectual property of Ayush Ghrit Kaushik.
# GitHub: https://github.com/Minato95-ayu
# 
# UNAUTHORIZED COPYING, REPRODUCTION, OR DISTRIBUTION IS STRICTLY PROHIBITED.
# ANY ATTEMPT TO CLONE OR CREATE DERIVATIVE WORKS FROM AAYU WILL BE SUBJECT
# TO LEGAL ACTION.
# ==============================================================================

import re

with open("runtime/vm/vm.py", "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace("self.heap = Heap()", "self.heap = Heap()\n        self.heap.set_vm(self)")

with open("runtime/vm/vm.py", "w", encoding="utf-8") as f:
    f.write(content)
print("vm.py updated")
