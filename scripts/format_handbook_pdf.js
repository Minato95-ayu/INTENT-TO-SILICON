const fs = require('fs');
const path = require('path');

const logoPath = path.join(__dirname, '..', 'assets', 'icons', 'aayu-dark.png');
const handbookPath = path.join(__dirname, '..', 'docs', 'AAYU_OFFICIAL_HANDBOOK.html');

const b64 = fs.readFileSync(logoPath).toString('base64');
let html = fs.readFileSync(handbookPath, 'utf8');

// 1. Embed real Base64 logo
html = html.replace(/<img class="cover-logo"[^>]*>/, '<img class="cover-logo" src="data:image/png;base64,' + b64 + '" alt="AAYU Logo">');

// 2. Adjust .cover-page CSS to prevent spill
const coverOld = /\.cover-page\s*\{[\s\S]*?page-break-after:\s*always;\s*break-after:\s*page;\s*\}/;
const coverNew = `.cover-page {
    box-sizing: border-box;
    min-height: 930px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background: linear-gradient(135deg, #090d16 0%, #111827 50%, #1e1b4b 100%);
    color: #ffffff;
    padding: 42px 38px;
    border-radius: 12px;
    page-break-after: always;
    break-after: page;
  }`;
html = html.replace(coverOld, coverNew);

// 3. Fix table CSS so it doesn't push entire tables across pages
html = html.replace(/table\s*\{[\s\S]*?break-inside:\s*avoid;\s*\}/, `table {
    width: 100%;
    border-collapse: collapse;
    margin: 12px 0 16px 0;
    font-size: 11.5px;
  }

  tr {
    break-inside: avoid;
  }`);

// 4. Add TOC styles if not present
if (!html.includes('.toc-grid')) {
  const extraStyles = `
  /* TOC 2-COLUMN GRID (FITS COMPLETELY ON PAGE 2) */
  .toc-container {
    page-break-after: always;
    break-after: page;
    padding-top: 2px;
  }

  .toc-h1 {
    font-size: 21px;
    font-weight: 800;
    color: #0f172a;
    border-bottom: 2.5px solid #6366f1;
    padding-bottom: 5px;
    margin-top: 0;
    margin-bottom: 5px;
    break-before: auto;
  }

  .toc-subtitle {
    color: #475569;
    font-size: 11.5px;
    margin-bottom: 12px;
  }

  .toc-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px 14px;
    margin-bottom: 12px;
  }

  .toc-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 3.5px solid #6366f1;
    border-radius: 5px;
    padding: 5px 9px;
    break-inside: avoid;
  }

  .toc-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1px;
  }

  .toc-chap-badge {
    font-size: 9.5px;
    font-weight: 700;
    color: #4f46e5;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .toc-chap-title {
    font-size: 11px;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.25;
  }

  .toc-chap-desc {
    font-size: 9.5px;
    color: #64748b;
    line-height: 1.3;
    margin-top: 1px;
  }
`;
  html = html.replace('</style>', extraStyles + '\n</style>');
}

// 5. Build TOC cards HTML
const chapters = [
  { num: 1, title: 'The 2026 Intent-to-Silicon Revolution', desc: 'Token optimization, AI Agent context waste, 2026 benchmark matrix.' },
  { num: 2, title: 'Terminal, PowerShell & Tooling', desc: 'CLI commands (run, build, --web), .ay/.aa/.aayu extensions, clean terminal.' },
  { num: 3, title: 'Compiler Architecture & 7-Stage Pipeline', desc: 'Pure AAYU lexer, parser, AST, analyzer, bytecode, register VM.' },
  { num: 4, title: 'Hello World & Syntax Anatomy', desc: 'First program, top-level statements, silent output guarantee.' },
  { num: 5, title: 'Variables, Memory & Primitive Types', desc: 'let, state, Int, Float, String, Bool, Null, scope and lifetime.' },
  { num: 6, title: 'Operators, Expressions & String Polymorphism', desc: 'Arithmetic, relational, logical, auto-coercion concatenation.' },
  { num: 7, title: 'Conditional Control Flow', desc: 'if, elif, else, end, multi-branch decision trees.' },
  { num: 8, title: 'Loops & Iteration', desc: 'while ... end, accumulators, infinite loop bounds and guards.' },
  { num: 9, title: 'Actions (Functions), Parameters & Scope', desc: 'First-class actions, call frames, parameter passing, recursion.' },
  { num: 10, title: 'Arrays & Dynamic Collections', desc: 'Dynamic lists, slicing, safe functional mutation via set_at.' },
  { num: 11, title: 'Dictionaries & Structured Records', desc: 'Key-value maps, JSON serialization, in-memory state tracking.' },
  { num: 12, title: 'Models & Built-In Database (AayuDb)', desc: 'RAM-First engine + WAL + SSD persistence, zero-config migrations.' },
  { num: 13, title: 'Web Routes, APIs & ASGI Microservices', desc: 'Declarative endpoints (get, post, put, delete), respond payload.' },
  { num: 14, title: 'Reactive UI & Single-File Components', desc: 'Declarative Flutter-like widget tree (Page, Column, Row, Button).' },
  { num: 15, title: 'The Cryptographic Engine', desc: 'High-entropy ASCII polynomial hashing, non-colliding SHA digests.' },
  { num: 16, title: 'Math & Computational Standard Library', desc: 'Fast square root, powers, absolute values, statistical math.' },
  { num: 17, title: 'Error Handling & Defensive Programming', desc: 'Guard clauses, safe fallbacks, schema validations.' },
  { num: 18, title: 'File I/O & Persistent Storage', desc: 'In-memory record stores, append-only logs, CSV/text pipelines.' },
  { num: 19, title: 'Data Structures & Algorithms (DSA)', desc: 'Searching, Sorting, Two-Pointers, Sliding Window, Stacks, Queues, DP.' },
  { num: 20, title: 'System Design & Enterprise Architecture', desc: 'Single-file architecture, In-memory WAL, High-concurrency async loop.' },
  { num: 21, title: '5 Production Projects & 20 Master Problems', desc: 'URL Shortener, Pub/Sub, Sentiment AI, E-Commerce, Auth + 20 Problems.' }
];

let tocCardsHtml = '<div class="toc-grid">\n';
chapters.forEach(c => {
  tocCardsHtml += `  <div class="toc-card">
    <div class="toc-card-header">
      <span class="toc-chap-badge">Chapter ${c.num}</span>
    </div>
    <div class="toc-chap-title">${c.title}</div>
    <div class="toc-chap-desc">${c.desc}</div>
  </div>\n`;
});
tocCardsHtml += '</div>';

const tocSectionRegex = /<!-- PAGE 2: TABLE OF CONTENTS -->[\s\S]*?<!-- CHAPTER 1 -->/;
const newTocSection = `<!-- PAGE 2: TABLE OF CONTENTS -->
<div class="toc-container">
  <h1 class="toc-h1">Table of Contents (All 21 Chapters)</h1>
  <p class="toc-subtitle">The complete 21-chapter engineering blueprint for the AAYU programming language:</p>

  ${tocCardsHtml}

  <div class="box-deepdive" style="margin-top: 8px; margin-bottom: 0;">
    <strong>How to use this Handbook:</strong> Every code snippet across all 21 chapters is verified on the native AAYU VM. Save any snippet with the <code>.ay</code> extension and run it immediately using <code>aayu filename.ay</code>.
  </div>
</div>

<!-- CHAPTER 1 -->`;

html = html.replace(tocSectionRegex, newTocSection);
fs.writeFileSync(handbookPath, html, 'utf8');
console.log('Handbook updated successfully! Output file size: ' + html.length + ' bytes');
