import React from "react";

export default function CommonErrorsPage() {
  return (
    <div className="prose prose-invert max-w-none">
      <h1>Common Errors in AAYU</h1>
      <p>
        AAYU is designed with developer experience at its core. Instead of cryptic stack traces,
        AAYU provides human-friendly error messages that point exactly to what went wrong and how to fix it.
      </p>

      <hr className="my-8 border-gray-800" />

      <h2>1. Variable Not Found</h2>
      <p>This happens when you try to use a variable or field before it has been defined.</p>
      
      <div className="bg-[#0D1117] border border-gray-800 rounded-lg p-4 my-4 font-mono text-sm">
        <div className="text-gray-400 mb-2">// Code</div>
        <div className="text-white mb-4">show unknown_user.</div>
        
        <div className="text-gray-400 mb-2">// Output</div>
        <div className="text-red-400 mb-1">🔴 [AAYU Runtime Error]</div>
        <div className="text-blue-400 mb-1">Line 1</div>
        <div className="text-white mb-4">Variable 'unknown_user' not found.</div>
        <div className="text-yellow-400 mb-1">🟡 Hint:</div>
        <div className="text-gray-300">Declare the variable before use.</div>
      </div>

      <hr className="my-8 border-gray-800" />

      <h2>2. Package Not Found</h2>
      <p>This happens when you try to import a module that hasn't been installed via the package manager.</p>
      
      <div className="bg-[#0D1117] border border-gray-800 rounded-lg p-4 my-4 font-mono text-sm">
        <div className="text-gray-400 mb-2">// Code</div>
        <div className="text-white mb-4">use payment.</div>
        
        <div className="text-gray-400 mb-2">// Output</div>
        <div className="text-red-400 mb-1">🔴 [AAYU Import Error]</div>
        <div className="text-blue-400 mb-1">Line 1</div>
        <div className="text-white mb-4">Module 'payment' not found.</div>
        <div className="text-yellow-400 mb-1">🟡 Hint:</div>
        <div className="text-gray-300">Did you forget to run 'aayu install payment'?</div>
      </div>

      <hr className="my-8 border-gray-800" />

      <h2>3. Missing Syntax Rules (e.g. Expected '.')</h2>
      <p>Every statement in AAYU must end with a period (`.`). The parser will immediately warn you if it's missing.</p>
      
      <div className="bg-[#0D1117] border border-gray-800 rounded-lg p-4 my-4 font-mono text-sm">
        <div className="text-gray-400 mb-2">// Code</div>
        <div className="text-white mb-4">task my_task</div>
        
        <div className="text-gray-400 mb-2">// Output</div>
        <div className="text-red-400 mb-1">🔴 [AAYU Syntax Error]</div>
        <div className="text-blue-400 mb-1">Line 1</div>
        <div className="text-white mb-4">Expect '.' after task declaration. Found 'EOF'</div>
      </div>
      
    </div>
  );
}
