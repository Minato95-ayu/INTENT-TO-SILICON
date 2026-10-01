import Link from 'next/link';
import { ArrowRight, Code2, Database, Layout, ShieldAlert } from 'lucide-react';

export default function ExamplesPage() {
  const examples = [
    {
      title: "AAYUGram (Social Network)",
      desc: "A full-stack Instagram clone built entirely in a single .aayu file. Features JWT Auth, SQLite Relational Models, Image Uploads, and a declarative feed UI.",
      tags: ["Full-Stack", "Auth", "UI Engine"],
      code: pp AAYUGram

model Post
    id Int
    image_url String
    caption String
    author_id Int
end

route "/api/feed"
    get
        let posts = Post.all()
        respond(posts)
    end
end

Page Feed
    Column
        Text("Your Feed", size: 24, bold: true)
        // Fetches directly via AAYU's SSR engine
        let items = fetch("/api/feed")
        List(items, item => PostCard(item))
    end
end

run Feed
    },
    {
      title: "AI Trading Bot",
      desc: "An algorithmic trading bot using AAYU's native Zero-Copy Tensors to compute moving averages and execute trades via WebSockets.",
      tags: ["AI/Tensors", "Math Engine", "WebSockets"],
      code: pp TradingBot

action compute_sma(prices: Tensor, window: Int) -> Tensor
    // Native PyTorch-style Tensor math
    let sma = prices.rolling_mean(window)
    return sma
end

route "wss://trade_stream"
    on_message(data)
        let prices = Tensor.new([100], data.history)
        let ma_fast = compute_sma(prices, 5)
        let ma_slow = compute_sma(prices, 20)
        
        if ma_fast.last() > ma_slow.last()
            print("BUY SIGNAL")
        end
    end
end
    }
  ];

  return (
    <main className="min-h-screen bg-[#050505] text-white pt-24 pb-16">
      <div className="container mx-auto px-4 max-w-7xl">
        
        <div className="text-center mb-20">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Enterprise <span className="text-cyan-400">Examples</span></h1>
          <p className="text-zinc-400 text-lg max-w-2xl mx-auto">
            See how AAYU scales to build massive, real-world microservices with built-in memory safety, Tensors, and zero dependencies.
          </p>
        </div>

        <div className="space-y-24">
          {examples.map((ex, i) => (
            <div key={i} className="grid lg:grid-cols-12 gap-12 items-center">
              
              <div className="lg:col-span-5">
                <div className="flex gap-2 mb-4">
                  {ex.tags.map(tag => (
                    <span key={tag} className="px-3 py-1 bg-white/5 border border-white/10 rounded-full text-xs font-mono text-zinc-400">
                      {tag}
                    </span>
                  ))}
                </div>
                <h2 className="text-3xl font-bold mb-4">{ex.title}</h2>
                <p className="text-zinc-400 leading-relaxed mb-8">{ex.desc}</p>
                <Link href="/tutorial" className="inline-flex items-center gap-2 text-cyan-400 hover:text-cyan-300 font-bold transition-colors">
                  Learn to build this <ArrowRight className="w-4 h-4" />
                </Link>
              </div>

              <div className="lg:col-span-7 relative">
                <div className="absolute -inset-2 bg-gradient-to-tr from-purple-500/10 to-cyan-500/10 rounded-3xl blur-xl" />
                <div className="relative bg-[#0a0a0a] border border-white/10 rounded-2xl overflow-hidden shadow-2xl">
                  <div className="flex items-center px-4 py-3 bg-[#111] border-b border-white/5">
                     <Code2 className="w-4 h-4 text-zinc-500 mr-2" />
                     <span className="text-xs font-mono text-zinc-400">example.aayu</span>
                  </div>
                  <pre className="p-6 font-mono text-sm leading-relaxed text-zinc-300 overflow-x-auto">
                    <code>{ex.code}</code>
                  </pre>
                </div>
              </div>

            </div>
          ))}
        </div>

      </div>
    </main>
  );
}
