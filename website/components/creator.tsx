/* eslint-disable */
﻿"use client";

import { motion } from "framer-motion";
import Image from "next/image";

export function Creator() {
  return (
    <section id="creator" className="py-24 border-t border-white/5 relative bg-zinc-950">
      <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-500/20 via-transparent to-red-500/20 blur-[100px]" />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="max-w-4xl mx-auto rounded-3xl border border-white/10 bg-black/50 p-8 md:p-12 backdrop-blur-xl shadow-2xl overflow-hidden relative">
          <div className="grid md:grid-cols-[1fr_2fr] gap-8 items-center">
            
            <div className="relative mx-auto w-48 h-48 md:w-full md:h-64 rounded-2xl overflow-hidden border border-white/20 bg-zinc-900 flex items-center justify-center p-4">
               <Image 
                  src="/aayu-logo.png" 
                  alt="AAYU Logo" 
                  width={200} 
                  height={200} 
                  className="object-contain"
               />
               <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent pointer-events-none" />
            </div>

            <div className="flex flex-col">
              <div className="inline-flex items-center rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-sm text-blue-300 mb-4 w-max">
                The Visionary Behind AAYU
              </div>
              <h2 className="text-3xl md:text-5xl font-bold mb-4 text-white">Ayush Kaushik</h2>
              <p className="text-lg text-zinc-300 leading-relaxed mb-6">
                "Software engineering is no longer about writing syntax. It's about translating human intent into deterministic, scalable architecture."
              </p>
              <p className="text-sm text-zinc-500 leading-relaxed">
                Ayush Kaushik designed AAYU from the ground up to be the first programming language built natively for the AI generation. Recognizing the limits of traditional languages, he pioneered the <strong>Intent Engine</strong> and <strong>BrainOS</strong>â€”creating an ecosystem where human thought transforms directly into production software.
              </p>
            </div>
            
          </div>
        </div>
      </div>
    </section>
  );
}

