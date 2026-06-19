import Link from "next/link";

const navItems = [
  { title: "Getting Started", href: "/docs/getting-started" },
  { title: "Installation", href: "/docs/installation" },
  { title: "Your First App", href: "/docs/first-app" },
  { title: "Tutorial: Todo App", href: "/docs/tutorials/todo-app" },
  { title: "Tutorial: Library System", href: "/docs/tutorials/library-system" },
  { title: "Reference: Syntax", href: "/docs/reference/syntax" },
  { title: "Reference: CLI", href: "/docs/reference/cli" },
  { title: "Reference: Package Manager", href: "/docs/reference/package-manager" },
  { title: "Reference: Common Errors", href: "/docs/reference/common-errors" },
  { title: "Showcase", href: "/docs/showcase" },
  { title: "Roadmap", href: "/docs/roadmap" },
];

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="max-w-7xl mx-auto px-6 w-full flex-1 flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-surface-border py-10 hidden md:block shrink-0">
        <div className="sticky top-24">
          <h4 className="font-semibold text-white mb-4 px-3 text-sm uppercase tracking-wider">Documentation</h4>
          <nav className="flex flex-col gap-1">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="px-3 py-2 text-sm text-gray-400 hover:text-white hover:bg-surface rounded-md transition-colors"
              >
                {item.title}
              </Link>
            ))}
          </nav>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 min-w-0 py-10 md:pl-12">
        {children}
      </div>
    </div>
  );
}
