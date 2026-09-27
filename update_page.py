with open("website/app/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

old_text = "The only language that speaks your mind."
new_text = """The only language that speaks your mind.
            <br />
            <div className="mt-6 flex flex-col items-center gap-2">
              <span className="text-emerald-400 font-bold bg-emerald-500/10 px-4 py-1.5 rounded-full border border-emerald-500/20 text-sm tracking-wide flex items-center gap-2">
                <Zap className="w-4 h-4" /> 100% SELF-HOSTING READY
              </span>
              <span className="text-zinc-500 text-xs font-mono">No Python runtime required. Lexer & Parser built natively in AAYU.</span>
            </div>"""

if old_text in content:
    content = content.replace(old_text, new_text)
    with open("website/app/page.tsx", "w", encoding="utf-8") as f:
        f.write(content)
    print("Website updated with Self-Hosting proof!")
else:
    print("Text not found in page.tsx")
