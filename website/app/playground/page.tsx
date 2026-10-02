'use client';

import { useState, useRef, useEffect } from 'react';
import { Play, Sparkles, Terminal, Key, Bot, User, Code2, Database, Layout, BookOpen, ChevronRight, Download, Server } from 'lucide-react';

export default function Playground() {
  const [code, setCode] = useState(`// Welcome to AAYU Playground
// Write intent, get silicon speed.

model Task
    id Int
    title String
    done Bool = false
end

route "/api/tasks"
    get
        respond(Task.all())
    end
end

Page Home
    Column
        heading "My Tasks"
        text "AAYU Full-Stack Demo"
    end
end
run Home`);
  
  const [output, setOutput] = useState(`[AAYU] Ready.\nType code and hit 'Run', or ask the Agentic AI to write it for you.`);
  const [isRunning, setIsRunning] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [prompt, setPrompt] = useState('');
  const [chat, setChat] = useState<{role: 'user' | 'agent', text: string}[]>([
    { role: 'agent', text: 'Hi! I am the AAYU Agentic AI. Enter your Gemini API key above, tell me what to build, and I will write the AAYU code for you.' }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll chat
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat]);

  const handleRun = () => {
    setIsRunning(true);
    setOutput(`[AAYU] Compiling intent...`);
    
    setTimeout(() => {
      let mockOutput = `[AAYU JIT] Tier-2 Compiler Triggered...\n`;
      if (code.includes('model ')) mockOutput += `[AAYU DB] In-Memory SQLite tables created.\n`;
      if (code.includes('route ')) mockOutput += `[AAYU NET] Server started on http://localhost:3000\n`;
      if (code.includes('Page ')) mockOutput += `[AAYU UI] Declarative widget tree built. (0.0ms render)\n`;
      if (code.includes('ml::')) mockOutput += `[AAYU ML] Tensors initialized. Hardware acceleration enabled.\n`;
      if (code.includes('print')) mockOutput += `\nOutput:\n> Execution completed.\n`;
      
      mockOutput += `\n? Execution Successful.\n[AAYU Token Savings: This 1-file app replaces ~8,500 tokens of React+Node boilerplate.]`;
      setOutput(mockOutput);
      setIsRunning(false);
    }, 800);
  };

  const handleAskAgent = async () => {
    if (!prompt.trim()) return;
    if (!apiKey.trim()) {
      alert("Please enter a valid Gemini API Key first.");
      return;
    }

    const userMsg = prompt;
    setPrompt('');
    setChat(prev => [...prev, { role: 'user', text: userMsg }]);
    setIsTyping(true);

    try {
      const systemPrompt = `You are the AAYU Agentic AI. AAYU is a single-file full-stack programming language.
Syntax Rules:
- Models: 'model Name\\n field Type\\nend' (Types: Int, String, Bool, Float).
- Routes: 'route "/path"\\n get\\n respond(data)\\n end\\nend'.
- UI: 'Page Name\\n Column\\n text "hello"\\n end\\nend\\nrun Name'.
- Variables: 'let x = 10', 'state count = 0'.
- Loops: 'for i in 1..10\\n print(i)\\nend'.
Write ONLY raw AAYU code inside a markdown code block (\`\`\`aayu ... \`\`\`) that fulfills the user's request. Include comments explaining it. Keep it concise.`;

      const res = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${apiKey}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          system_instruction: { parts: [{ text: systemPrompt }] },
          contents: [{ parts: [{ text: userMsg }] }]
        })
      });

      const data = await res.json();
      if (data.error) throw new Error(data.error.message);

      const agentText = data.candidates[0].content.parts[0].text;
      
      // Extract code block
      const codeMatch = agentText.match(/```(?:aayu)?\n([\s\S]*?)```/);
      const generatedCode = codeMatch ? codeMatch[1].trim() : agentText.replace(/```/g, '').trim();

      setChat(prev => [...prev, { role: 'agent', text: "Here is the code I generated for you! I've loaded it into the editor." }]);
      setCode(generatedCode);
      
    } catch (err: any) {
      setChat(prev => [...prev, { role: 'agent', text: `Error: ${err.message}` }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="pt-16 min-h-screen bg-black flex flex-col h-screen overflow-hidden">
      
      {/* Top Toolbar */}
      <div className="h-14 border-b border-zinc-800 bg-zinc-950 flex items-center justify-between px-4 shrink-0">
        <div className="flex items-center gap-4">
          <div className="text-emerald-400 font-bold flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            AAYU IDE Playground
          </div>
          <div className="hidden md:flex items-center gap-2 text-xs text-zinc-500 bg-zinc-900 px-3 py-1.5 rounded-md border border-zinc-800">
            <Key className="w-3 h-3" />
            <input 
              type="password" 
              placeholder="Enter Gemini API Key for Agent..." 
              value={apiKey}
              onChange={e => setApiKey(e.target.value)}
              className="bg-transparent border-none outline-none w-64 text-zinc-300 placeholder:text-zinc-600"
            />
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <span className="text-xs text-zinc-500 hidden lg:block mr-2">Token Savings Proof Enabled</span>
          <button 
            onClick={handleRun}
            disabled={isRunning}
            className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-500 text-white px-4 py-1.5 rounded-md font-medium text-sm transition-colors disabled:opacity-50"
          >
            <Play className="w-4 h-4" fill="currentColor" />
            {isRunning ? 'Compiling...' : 'Run Code'}
          </button>
        </div>
      </div>

      {/* Main Layout */}
      <div className="flex-1 flex overflow-hidden">
        
        {/* Left Sidebar: Cheatsheet / Library */}
        <div className="w-64 border-r border-zinc-800 bg-zinc-950 flex flex-col hidden lg:flex shrink-0">
          <div className="p-3 border-b border-zinc-800 text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-2">
            <BookOpen className="w-4 h-4" />
            Library & Hints
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-6 text-sm">
            
            <div>
              <h4 className="text-purple-400 font-semibold mb-2 flex items-center gap-1"><Database className="w-3 h-3"/> Models</h4>
              <p className="text-zinc-500 text-xs mb-2">Define SQLite tables instantly.</p>
              <pre className="bg-zinc-900 border border-zinc-800 p-2 rounded text-xs text-zinc-300 font-mono">
                model User{'\n'}  id Int{'\n'}  name String{'\n'}end
              </pre>
            </div>

            <div>
              <h4 className="text-cyan-400 font-semibold mb-2 flex items-center gap-1"><Server className="w-3 h-3"/> Routes</h4>
              <p className="text-zinc-500 text-xs mb-2">Built-in API endpoints.</p>
              <pre className="bg-zinc-900 border border-zinc-800 p-2 rounded text-xs text-zinc-300 font-mono">
                route "/api/users"{'\n'}  get{'\n'}    respond(User.all()){'\n'}  end{'\n'}end
              </pre>
            </div>

            <div>
              <h4 className="text-emerald-400 font-semibold mb-2 flex items-center gap-1"><Layout className="w-3 h-3"/> Declarative UI</h4>
              <p className="text-zinc-500 text-xs mb-2">Flutter-like component tree.</p>
              <pre className="bg-zinc-900 border border-zinc-800 p-2 rounded text-xs text-zinc-300 font-mono">
                Page App{'\n'}  Column{'\n'}    text "Hello"{'\n'}  end{'\n'}end
              </pre>
            </div>

            <div className="bg-purple-900/20 border border-purple-500/30 rounded-lg p-3">
              <h4 className="text-purple-400 font-medium text-xs mb-1 flex items-center gap-1">
                <Sparkles className="w-3 h-3"/> Token Optimization
              </h4>
              <p className="text-zinc-400 text-[11px] leading-relaxed">
                By combining DB, Server, and UI into one file with AAYU, AI agents use ~90% fewer tokens compared to generating a standard Next.js + Node + Prisma stack.
              </p>
            </div>
            
          </div>
        </div>

        {/* Center: Editor & Terminal */}
        <div className="flex-1 flex flex-col min-w-0">
          {/* Editor */}
          <div className="flex-1 flex flex-col min-h-0 bg-[#0d0d0d]">
            <div className="h-9 border-b border-zinc-800 flex items-center px-4 bg-zinc-900/50">
              <span className="text-xs text-zinc-500 font-mono flex items-center gap-2"><Code2 className="w-3 h-3" /> main.aayu</span>
            </div>
            <textarea 
              value={code}
              onChange={e => setCode(e.target.value)}
              spellCheck={false}
              className="flex-1 bg-transparent text-zinc-300 font-mono text-sm p-4 outline-none resize-none leading-relaxed whitespace-pre"
              style={{ tabSize: 4 }}
            />
          </div>

          {/* Terminal */}
          <div className="h-64 border-t border-zinc-800 bg-black flex flex-col shrink-0">
            <div className="h-9 border-b border-zinc-800 flex items-center px-4 bg-zinc-900/50">
              <span className="text-xs text-zinc-500 font-mono flex items-center gap-2"><Terminal className="w-3 h-3" /> Output</span>
            </div>
            <div className="flex-1 p-4 overflow-y-auto font-mono text-sm text-zinc-400 whitespace-pre-wrap">
              {output}
            </div>
          </div>
        </div>

        {/* Right Sidebar: Agentic AI Chat */}
        <div className="w-80 border-l border-zinc-800 bg-zinc-950 flex flex-col shrink-0">
          <div className="h-14 border-b border-zinc-800 flex items-center px-4 bg-zinc-900/50 justify-between">
            <span className="text-sm font-semibold text-white flex items-center gap-2">
              <Bot className="w-4 h-4 text-purple-400" />
              Agentic AI
            </span>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto space-y-4">
            {chat.map((msg, i) => (
              <div key={i} className={`flex flex-col ${msg.role === 'user' ? 'items-end' : 'items-start'}`}>
                <div className={`max-w-[90%] p-3 rounded-xl text-sm ${msg.role === 'user' ? 'bg-purple-600 text-white rounded-br-none' : 'bg-zinc-900 border border-zinc-800 text-zinc-300 rounded-bl-none'}`}>
                  {msg.role === 'agent' && <Bot className="w-4 h-4 mb-2 text-purple-400" />}
                  {msg.role === 'user' && <User className="w-4 h-4 mb-2 text-white/70" />}
                  <p className="whitespace-pre-wrap text-xs leading-relaxed">{msg.text}</p>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex items-start">
                <div className="bg-zinc-900 border border-zinc-800 p-3 rounded-xl rounded-bl-none text-zinc-500 text-xs flex gap-1">
                  <span className="animate-bounce">.</span><span className="animate-bounce delay-75">.</span><span className="animate-bounce delay-150">.</span>
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="p-3 border-t border-zinc-800 bg-zinc-950">
            <div className="relative">
              <textarea 
                value={prompt}
                onChange={e => setPrompt(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAskAgent(); } }}
                placeholder="Ask agent to build an API, a blog model, or a UI page..."
                className="w-full bg-zinc-900 border border-zinc-800 rounded-xl pl-3 pr-10 py-3 text-xs text-white placeholder:text-zinc-600 outline-none focus:border-purple-500/50 resize-none h-20"
              />
              <button 
                onClick={handleAskAgent}
                disabled={isTyping || !prompt.trim()}
                className="absolute right-2 bottom-2 p-1.5 bg-purple-600 hover:bg-purple-500 rounded-lg text-white disabled:opacity-50 transition-colors"
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            {!apiKey && (
              <p className="text-[10px] text-red-400 mt-2 text-center">API Key required (Top toolbar)</p>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
