import React from 'react';

export default function TermsPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">Terms of Service</h1>
        <p className="text-zinc-400 mb-4">Last updated: {new Date().toLocaleDateString()}</p>
        <div className="text-zinc-300 space-y-4">
          <p>AAYU is provided under the MIT License.</p>
          <p>You are free to use, modify, and distribute AAYU for commercial and non-commercial purposes, provided the original copyright notice is included.</p>
        </div>
      </div>
    </main>
  );
}
