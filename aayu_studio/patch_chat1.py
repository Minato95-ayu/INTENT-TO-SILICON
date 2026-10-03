import os

filepath = 'D:/Topptic/app/components/ai/ChatPanel.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update the introduction text
old_intro = 'dY< **Topptic AI ?" Agentic Coding Engine**'
new_intro = '🚀 **AAYU Studio AI — Expert Agent**\\n\\nNamaste! Main aapka **AAYU AI** hoon — ek fully agentic coding assistant jo directly aapke workspace mein AAYU files likh sakta hai, AAYU commands execute kar sakta hai, aur AAYU bugs auto-fix kar sakta hai.\\n\\n**Main ye sab kar sakta hoon:**\\n* 📝 AAYU files create/edit karna\\n* 💻 AAYU VM commands run karna\\n* 🐛 Bugs detect aur auto-fix karna\\n* 🏗️ AAYU apps scaffold karna\\n\\nSettings me apni API Key dalo aur shuru ho jao!'
content = content.replace(old_intro, new_intro)

# 2. Update System Prompt
old_prompt = "You are Topptic's offline agentic coding assistant."
new_prompt = '''You are AAYU Studio's Expert AI Coder. You specialize in the AAYU programming language. You write highly optimized single-file full-stack code using AAYU. When the user asks for a website, app, or ML model, you only output valid .aayu code.'''
content = content.replace(old_prompt, new_prompt)

# 3. Inject API Keys UI state
import re
state_injection = '''
  const [messages, setMessages] = useState<AIChatMessage[]>([
'''
state_new = '''
  const [provider, setProvider] = useState('Ollama');
  const [apiKey, setApiKey] = useState('');
  
  const [messages, setMessages] = useState<AIChatMessage[]>([
'''
content = content.replace(state_injection, state_new)

# 4. Inject Settings UI right below the chat header
header_find = '''<div className="flex items-center gap-2 mb-2">
            <h2 className="text-[10px] font-black uppercase tracking-widest text-slate-300">Topptic AI</h2>
            <div className="px-1.5 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider bg-purple-500/10 text-purple-400 border border-purple-500/20">
              Agentic
            </div>
          </div>'''
header_new = '''<div className="flex items-center gap-2 mb-2 justify-between">
            <div className="flex items-center gap-2">
              <h2 className="text-[10px] font-black uppercase tracking-widest text-slate-300">AAYU AI Agent</h2>
              <div className="px-1.5 py-0.5 rounded text-[8px] font-bold uppercase tracking-wider bg-purple-500/10 text-purple-400 border border-purple-500/20">
                Agentic
              </div>
            </div>
            <div className="flex items-center gap-2">
              <select value={provider} onChange={(e) => setProvider(e.target.value)} className="bg-slate-800 border-none rounded text-xs text-white p-1">
                <option value="Ollama">Ollama (Local)</option>
                <option value="OpenAI">OpenAI</option>
                <option value="Anthropic">Anthropic</option>
                <option value="Gemini">Gemini</option>
              </select>
              {provider !== 'Ollama' && (
                <input 
                  type="password" 
                  placeholder="API Key" 
                  value={apiKey} 
                  onChange={(e) => setApiKey(e.target.value)} 
                  className="bg-slate-800 border-none rounded text-xs text-white p-1 w-24"
                />
              )}
            </div>
          </div>'''
content = content.replace(header_find, header_new)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
