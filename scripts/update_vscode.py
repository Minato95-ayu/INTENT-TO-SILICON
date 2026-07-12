import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\vscode\page.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the two buttons with authenticity-enforced ones
old_buttons = '''
            <div className="flex flex-wrap gap-4">
              <Button className="bg-blue-600 hover:bg-blue-500 text-white gap-2">
                <Download className="w-4 h-4" /> Install from Marketplace
              </Button>
              <Button variant="outline" className="border-white/10 hover:bg-white/5 bg-transparent gap-2">
                Download .vsix
              </Button>
            </div>
'''

new_buttons = '''
            <div className="flex flex-wrap gap-4 relative group">
              <Button disabled className="bg-blue-600/50 text-white/50 gap-2 cursor-not-allowed">
                <Download className="w-4 h-4" /> Install from Marketplace
              </Button>
              <Button disabled variant="outline" className="border-white/10 bg-transparent gap-2 text-zinc-500 cursor-not-allowed">
                Download .vsix
              </Button>
              <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none">
                <span className="px-3 py-1 bg-black border border-yellow-500/50 text-yellow-500 text-xs font-bold rounded shadow-xl">Available in v1.0 Release</span>
              </div>
            </div>
'''

content = content.replace(old_buttons.strip(), new_buttons.strip())

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated vscode page with Authenticity rule.")
