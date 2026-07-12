 

export default function Page() {
  return (
    <main className="min-h-screen bg-black text-white flex items-center justify-center pt-24 pb-16">
      <div className="container mx-auto px-4 text-center">
        <h1 className="text-4xl md:text-6xl font-bold tracking-tight mb-6">
          Blog
        </h1>
        <p className="text-xl text-zinc-400 max-w-2xl mx-auto mb-8">
          This section is currently under development for the v1.0 release.
        </p>
        <div className="inline-block rounded-full border border-blue-500/30 bg-blue-500/10 px-4 py-1.5 text-sm font-medium text-blue-300">
          Available Now
        </div>
      </div>
    </main>
  );
}
