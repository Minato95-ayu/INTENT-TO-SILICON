import React from 'react';

export default function PrivacyPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">Privacy Policy</h1>
        <p className="text-zinc-400 mb-4">Last updated: {new Date().toLocaleDateString()}</p>
        <div className="text-zinc-300 space-y-4">
          <p>We respect your privacy. The AAYU compiler runs entirely locally on your machine and does not phone home, track usage, or upload your source code.</p>
          <p>This website uses Vercel Analytics for basic non-identifiable web traffic statistics.</p>
        </div>
      </div>
    </main>
  );
}
