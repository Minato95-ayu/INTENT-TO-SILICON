import os

p = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\page.tsx'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# I will find the 'The Developer Ecosystem' section and replace it, but since I rewrote the homepage entirely to the Dashboard layout in the last step, I need to check if that section still exists.
