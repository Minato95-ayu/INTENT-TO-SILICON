---
layout: home

hero:
  name: "AAYU"
  text: "Human Readable Programming Language"
  tagline: "The world's first Intent-to-Silicon Platform"
  actions:
    - theme: brand
      text: Get Started
      link: /guide/installation
    - theme: alt
      text: View Documentation
      link: /guide/basics

features:
  - title: Intent Engine
    details: Build entire full-stack applications instantly from natural language using 'aayu build'.
  - title: Natural Syntax
    details: Code that reads like a natural sentence. Zero boilerplate, zero confusing symbols.
  - title: Built-in Ecosystem
    details: Web server, database, authentication, and AI tools built directly into the standard library.
---

<style>
:root {
  --vp-c-brand-1: #6E56CF;
  --vp-c-brand-2: #8974e6;
  --vp-c-brand-3: #5840b5;
}
.demo-box {
  background: #1e1e1e;
  border-radius: 8px;
  padding: 2rem;
  color: #fff;
  font-family: monospace;
  margin-top: 4rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.demo-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--vp-c-brand-1);
}
.command { color: #4ade80; }
.output { color: #9ca3af; margin-top: 1rem; line-height: 1.6; }
</style>

<div class="demo-box">
  <div class="demo-title">Build a Full-Stack App in 10 Seconds</div>
  <div class="command">$ aayu build "Build a Library Management System"</div>
  <div class="output">
    [1/3] Understanding Intent...<br>
    [2/3] Resolving Architecture (Book, Member, BorrowRecord)...<br>
    [3/3] Emitting Full Stack AAYU Code...<br><br>
    <span style="color: #60a5fa">✔ Generated main.aayu</span><br>
    <span style="color: #60a5fa">✔ Generated database schema</span><br>
    <span style="color: #60a5fa">✔ Generated views/dashboard.html</span><br>
    <span style="color: #60a5fa">✔ Generated views/books.html</span><br><br>
    Server running at http://localhost:8080
  </div>
</div>
