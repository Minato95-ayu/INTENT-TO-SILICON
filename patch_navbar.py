with open("website/components/navbar.tsx", "r") as f:
    text = f.read()

target1 = '<Link href="/tutorial" className="hover:text-white transition-colors text-purple-400 font-bold">Tutorial</Link>'
replacement1 = '<Link href="/tutorial" className="hover:text-white transition-colors text-purple-400 font-bold">Tutorial</Link>\n            <Link href="/reports" className="hover:text-white transition-colors text-cyan-400 font-bold">Benchmarks & Proofs</Link>'

target2 = '<Link href="/tutorial" onClick={() => setMobileMenuOpen(false)} className="text-purple-400 font-bold hover:text-purple-300 transition-colors block">Tutorial</Link>'
replacement2 = '<Link href="/tutorial" onClick={() => setMobileMenuOpen(false)} className="text-purple-400 font-bold hover:text-purple-300 transition-colors block">Tutorial</Link>\n          <Link href="/reports" onClick={() => setMobileMenuOpen(false)} className="text-cyan-400 font-bold hover:text-cyan-300 transition-colors block">Benchmarks & Proofs</Link>'

text = text.replace(target1, replacement1)
text = text.replace(target2, replacement2)

with open("website/components/navbar.tsx", "w") as f:
    f.write(text)

print("Navbar updated")
