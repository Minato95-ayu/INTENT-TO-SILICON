 
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/navbar";
import { Footer } from "@/components/footer";
import { GlobalSearch } from "@/components/global-search";const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "AAYU",
  description: "AAYU is a modern, simple, fast, offline-first, and AI-native programming language. Build production apps by defining human intent.",
  openGraph: {
    title: "AAYU | Human Intent Programming",
    description: "Write less. Build more. AAYU is an intent-first programming language with a built-in BrainOS for autonomous software engineering.",
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
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-black text-white min-h-screen`}
      >
        <div className="relative flex min-h-screen flex-col">
          <Navbar />
          <GlobalSearch />
          {children}
          <Footer />
        </div>
      </body>
    </html>
  );
}
