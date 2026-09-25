import React from 'react';
import { Code } from 'lucide-react';

export default function ExamplesPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-5xl">
        <h1 className="text-5xl font-bold mb-6">Examples Gallery</h1>
        <p className="text-xl text-zinc-400 mb-12">Real-world applications built with AAYU.</p>
        <div className="bg-[#050505] border border-white/10 rounded-2xl p-8 mb-8">
          <h2 className="text-2xl font-bold mb-4">AAYUGram (Full-Stack Social App)</h2>
          <pre className="text-zinc-300 font-mono text-sm">
{`app AAYUGram

model Post
    id Int
    content String
end

route "/feed"
    get
        respond(Post.all())
    end
end

run AAYUGram`}
          </pre>
        </div>
      </div>
    </main>
  );
}
