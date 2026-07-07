 
import Link from "next/link";
import { languageNavData } from "@/data/language";

export default function LanguageLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="min-h-screen bg-black text-white pt-16">
      <div className="container mx-auto px-4 max-w-7xl flex">
        {/* Sidebar Navigation */}
        <aside className="w-64 flex-shrink-0 py-10 pr-6 hidden lg:block border-r border-white/10 overflow-y-auto" style={{ height: 'calc(100vh - 64px)', position: 'sticky', top: '64px' }}>
          <h2 className="text-xl font-bold mb-8">Language Portal</h2>
          <nav className="space-y-8">
            {languageNavData.map((section, idx) => (
              <div key={idx}>
                <h4 className="font-semibold text-zinc-100 mb-3 text-sm tracking-wider uppercase">{section.title}</h4>
                <ul className="space-y-2 text-sm text-zinc-400">
                  {section.items.map((item, itemIdx) => (
                    <li key={itemIdx}>
                      <Link href={`/language/${item.slug}`} className="hover:text-blue-400 transition-colors block py-1">
                        {item.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </nav>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 py-10 lg:pl-12 overflow-x-hidden">
          {children}
        </main>
      </div>
    </div>
  );
}
