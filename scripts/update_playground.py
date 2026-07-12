import os

filepath = r'd:\intent-to-silicon-research\INTENT-TO-SILICON\website\app\playground\page.tsx'

playground_code = '''
"use client";

import { useState } from "react";
import { Play, Terminal, Database, Code2, Network, Cpu, FileJson, Hash, Bot, ListTree, Activity } from "lucide-react";
import { Button } from "@/components/ui/button";

const TABS = [
  { id: "editor", icon: Code2, label: "Editor" },
  { id: "tokens", icon: Hash, label: "Tokens" },
  { id: "ast", icon: ListTree, label: "AST" },
  { id: "intent", icon: Network, label: "Intent Graph" },
  { id: "ir", icon: FileJson, label: "IR" },
  { id: "bytecode", icon: Terminal, label: "Bytecode" },
  { id: "llvm", icon: Cpu, label: "LLVM IR" },
  { id: "brainos", icon: Bot, label: "BrainOS Review" },
  { id: "runtime", icon: Database, label: "Runtime Memory" },
  { id: "console", icon: Activity, label: "Console" },
];

export default function PlaygroundPage() {
  const [activeTab, setActiveTab] = useState("editor");
  const [code, setCode] = useState(// Welcome to the AAYU Playground
entity User
has
    id: Number
    name: Text
end.

extend User
has
    fn greet() -> Text
    do
        return "Hello, " + self.name.
    end.
end.

let u = User { id: 1, name: "Developer" }.
print(u.greet()).
);

  const [isCompiling, setIsCompiling] = useState(false);
  const [output, setOutput] = useState<{tab: string, data: string}[]>([]);

  const handleRun = () => {
    setIsCompiling(true);
    setActiveTab("console");
    setTimeout(() => {
      setOutput([
        { tab: "tokens", data: "Token(KEYWORD, 'entity')\\nToken(IDENTIFIER, 'User')\\nToken(KEYWORD, 'has')\\nToken(IDENTIFIER, 'id')\\nToken(COLON, ':')\\n..." },
        { tab: "ast", data: "{\\n  \\"type\\": \\"Program\\",\\n  \\"body\\": [\\n    { \\"type\\": \\"EntityDeclaration\\", \\"name\\": \\"User\\" }\\n  ]\\n}" },
        { tab: "intent", data: "Node: User (Entity)\\nEdges:\\n  - hasMethod: greet() -> Text\\n  - hasField: id (Number)\\n  - hasField: name (Text)" },
        { tab: "ir", data: "define User_greet(%User* %self) {\\n  %1 = load %self.name\\n  %2 = call StringConcat(\\"Hello, \\", %1)\\n  ret %2\\n}" },
        { tab: "bytecode", data: "0000: OP_LOAD_CONST 1 (\\"Hello, \\")\\n0002: OP_LOAD_ATTR 'name'\\n0004: OP_STR_CONCAT\\n0005: OP_RETURN" },
        { tab: "llvm", data: "; ModuleID = 'AAYU_Main'\\nsource_filename = \\"main.aayu\\"\\n\\ndefine { i8*, i64 } @User_greet({ i8*, i64 }* %self) {\\nentry:\\n  ret { i8*, i64 } { i8* getelementptr inbounds ([8 x i8], [8 x i8]* @.str, i32 0, i32 0), i64 7 }\\n}" },
        { tab: "brainos", data: "BrainOS Architecture Review:\\n✅ Entity 'User' is structurally sound.\\n⚠️ Notice: String concatenation in greet() allocates memory. Consider using a String Builder if called in a tight loop." },
        { tab: "runtime", data: "Memory Dump:\\nHeap Region 0x01:\\n  [0x0100] User { id: 1, name: ptr(0x0120) }\\n  [0x0120] \\"Developer\\" (RefCnt: 1)\\n  [0x0140] \\"Hello, Developer\\" (RefCnt: 0 -> GC Queued)" },
        { tab: "console", data: "> aayu run main.aayu\\n\\nHello, Developer\\n\\n[Process exited with code 0]" }
      ]);
      setIsCompiling(false);
    }, 1500);
  };

  const getTabData = (tabId: string) => {
    if (tabId === "editor") return code;
    const found = output.find(o => o.tab === tabId);
    return found ? found.data : "No data. Click 'Run' to generate.";
  };

  return (
    <main className="h-screen flex flex-col bg-[#050505] text-white pt-16">
      <div className="flex items-center justify-between px-6 py-3 border-b border-white/10 bg-[#0a0a0a]">
        <div className="font-bold flex items-center gap-2">
          <Code2 className="w-5 h-5 text-blue-400" /> Playground
        </div>
        <Button 
          onClick={handleRun}
          disabled={isCompiling}
          className="bg-green-600 hover:bg-green-500 text-white font-bold h-8 px-6 gap-2"
        >
          <Play className="w-4 h-4 fill-current" /> {isCompiling ? "Compiling..." : "Run"}
        </Button>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Left: Editor Tab Buttons */}
        <div className="w-48 bg-[#0a0a0a] border-r border-white/10 flex flex-col overflow-y-auto">
          {TABS.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={lex items-center gap-3 px-4 py-3 text-sm font-medium border-l-2 transition-colors \}
            >
              <tab.icon className="w-4 h-4" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Right: Content Area */}
        <div className="flex-1 bg-[#1e1e1e] relative">
          {activeTab === "editor" ? (
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              className="w-full h-full bg-transparent text-zinc-300 font-mono text-sm p-6 outline-none resize-none"
              spellCheck={false}
            />
          ) : (
            <div className="w-full h-full overflow-auto p-6 font-mono text-sm">
              <pre className={activeTab === 'console' ? 'text-green-400' : 'text-zinc-400'}>
                {getTabData(activeTab)}
              </pre>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
'''

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(playground_code)

print("Updated Playground to 10 tabs.")
