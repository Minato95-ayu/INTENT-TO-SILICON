/* eslint-disable */
"use client";

import { useState } from "react";
import { Search, Package, ShieldCheck, Download, Star } from "lucide-react";
import { Button } from "@/components/ui/button";

const OFFICIAL_PACKAGES = [
  { name: "aayu/http", desc: "High-performance HTTP client and server for the AAYU ecosystem.", version: "1.0.0", downloads: "1.2M", stars: "4.5k" },
  { name: "aayu/json", desc: "Fast JSON parsing and serialization built into the core.", version: "1.0.0", downloads: "2.1M", stars: "5.1k" },
  { name: "aayu/crypto", desc: "Standard cryptographic primitives and hashing algorithms.", version: "1.0.0", downloads: "800k", stars: "3.2k" },
];

const COMMUNITY_PACKAGES = [
  { name: "db_driver_pg", desc: "PostgreSQL driver with connection pooling and async queries.", author: "johndoe", version: "0.4.1", downloads: "45k", stars: "340" },
  { name: "jwt_auth", desc: "JSON Web Token generation and validation middleware.", author: "security_ninja", version: "2.1.0", downloads: "120k", stars: "890" },
  { name: "graphql_core", desc: "GraphQL schema builder and executor for AAYU.", author: "gql_fan", version: "1.2.4", downloads: "89k", stars: "670" },
];

const CATEGORIES = ["All", "Web", "Database", "Security", "AI", "Testing", "CLI", "Data Science"];

export default function PackagesPage() {
  const [search, setSearch] = useState("");
  const [activeCategory, setActiveCategory] = useState("All");

  return (
    <main className="min-h-screen bg-black text-white pt-24 pb-20">
      <div className="container mx-auto px-4 max-w-6xl">
        
        {/* Header & Search */}
        <div className="flex flex-col items-center text-center mb-16">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">
            AAYU Package Registry
          </h1>
          <p className="text-lg text-zinc-400 max-w-2xl mb-8">
            Discover, install, and publish offline-first packages for the AAYU ecosystem.
          </p>
          
          <div className="relative w-full max-w-2xl">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 h-5 w-5 text-zinc-500" />
            <input 
              type="text" 
              placeholder="Search for packages (e.g., http, database...)" 
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full h-14 pl-12 pr-4 rounded-full bg-white/5 border border-white/10 focus:border-blue-500/50 focus:bg-white/10 outline-none transition-all text-white placeholder:text-zinc-600"
            />
          </div>
        </div>

        {/* Categories */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-12">
          {CATEGORIES.map(cat => (
            <button 
              key={cat}
              onClick={() => setActiveCategory(cat)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                activeCategory === cat 
                  ? "bg-blue-600 text-white" 
                  : "bg-white/5 text-zinc-400 hover:bg-white/10 hover:text-white"
              }`}
            >
              {cat}
            </button>
          ))}
        </div>

        {/* Official Packages */}
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <ShieldCheck className="text-blue-400" /> 
            Official Core Packages
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {OFFICIAL_PACKAGES.map(pkg => (
              <div key={pkg.name} className="p-6 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition-colors group cursor-pointer">
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-mono text-lg text-blue-300 font-semibold">{pkg.name}</h3>
                  <span className="text-xs font-mono text-zinc-500 bg-black/50 px-2 py-1 rounded">{pkg.version}</span>
                </div>
                <p className="text-sm text-zinc-400 mb-6 min-h-[40px]">{pkg.desc}</p>
                <div className="flex items-center gap-4 text-xs text-zinc-500 font-medium">
                  <span className="flex items-center gap-1"><Download className="h-3 w-3" /> {pkg.downloads}</span>
                  <span className="flex items-center gap-1"><Star className="h-3 w-3" /> {pkg.stars}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Community Packages */}
        <div>
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Package className="text-purple-400" /> 
            Trending Community Packages
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {COMMUNITY_PACKAGES.map(pkg => (
              <div key={pkg.name} className="p-6 rounded-xl border border-white/10 bg-white/5 hover:bg-white/10 transition-colors group cursor-pointer">
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="font-mono text-lg text-purple-300 font-semibold">{pkg.name}</h3>
                    <p className="text-xs text-zinc-500 mt-1">by <span className="text-zinc-400">{pkg.author}</span></p>
                  </div>
                  <span className="text-xs font-mono text-zinc-500 bg-black/50 px-2 py-1 rounded">{pkg.version}</span>
                </div>
                <p className="text-sm text-zinc-400 mb-6 min-h-[40px]">{pkg.desc}</p>
                <div className="flex items-center gap-4 text-xs text-zinc-500 font-medium">
                  <span className="flex items-center gap-1"><Download className="h-3 w-3" /> {pkg.downloads}</span>
                  <span className="flex items-center gap-1"><Star className="h-3 w-3" /> {pkg.stars}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
    </main>
  );
}
