import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Link from "next/link";
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Aayu | Intent-Driven Programming Language",
  description: "A simple, highly readable language built for developers bridging human intent to silicon execution.",
  keywords: ["Aayu", "Programming Language", "Intent-Driven", "Web Framework", "Syntax"],
  authors: [{ name: "Ayush" }],
  openGraph: {
    title: "Aayu | Intent-Driven Programming Language",
    description: "A simple, highly readable language built for developers bridging human intent to silicon execution.",
    url: "https://minato95-ayu.github.io/AAYU/",
    siteName: "Aayu Language",
    images: [
      {
        url: "/logo.jpg",
        width: 1024,
        height: 1024,
      },
    ],
    locale: "en_US",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased min-h-screen flex flex-col`}
      >
        <header className="sticky top-0 z-50 glass border-b border-surface-border">
          <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 text-xl font-bold text-white tracking-wide">
              <img src="/logo.jpg" alt="Aayu Logo" className="h-8 w-8 object-contain" />
              <span>Aayu<span className="text-primary">.</span></span>
            </Link>
            <nav className="flex items-center gap-6">
              <Link href="/docs/getting-started" className="text-sm font-medium hover:text-white transition-colors">
                Docs
              </Link>
              <Link href="/docs/roadmap" className="text-sm font-medium hover:text-white transition-colors">
                Roadmap
              </Link>
              <a href="https://github.com/ayush/aayu" target="_blank" rel="noopener noreferrer" className="text-sm font-medium hover:text-white transition-colors">
                GitHub
              </a>
            </nav>
          </div>
        </header>
        <main className="flex-1 flex flex-col">
          {children}
        </main>
      </body>
    </html>
  );
}
