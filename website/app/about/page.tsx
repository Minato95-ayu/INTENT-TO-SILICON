import React from 'react';
import Link from 'next/link';

export default function AboutPage() {
  return (
    <main className="min-h-screen pt-32 pb-20">
      <div className="container mx-auto px-4 max-w-4xl text-center">
        <h1 className="text-5xl font-bold mb-6">About Us</h1>
        <p className="text-xl text-zinc-400 mb-12">
          AAYU is an open-source project founded and engineered by Ayush Ghrit Kaushik.
        </p>
        <Link href="/" className="text-blue-400 hover:underline text-lg">
          Return to Homepage to learn more about the creator.
        </Link>
      </div>
    </main>
  );
}
