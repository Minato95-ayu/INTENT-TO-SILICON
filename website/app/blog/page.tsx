import React from 'react';
import { Newspaper } from 'lucide-react';

export default function BlogPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-5xl font-bold mb-6">AAYU Blog</h1>
        <p className="text-xl text-zinc-400 mb-12">The latest news, updates, and engineering deep-dives from the AAYU team.</p>
        
        <div className="bg-[#050505] border border-white/10 rounded-2xl p-8">
          <span className="text-blue-500 text-sm font-bold tracking-wider uppercase mb-2 block">Announcement</span>
          <h2 className="text-3xl font-bold mb-4">Welcome to AAYU v1.0</h2>
          <p className="text-zinc-400 mb-6">Today we are thrilled to announce the official open-source release of AAYU, the world's first Intent-to-Silicon programming language...</p>
          <span className="text-zinc-500 text-sm">Published by Ayush Ghrit Kaushik</span>
        </div>
      </div>
    </main>
  );
}
