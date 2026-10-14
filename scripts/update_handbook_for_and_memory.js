const fs = require('fs');
const path = require('path');

const handbookPath = path.join(__dirname, '..', 'docs', 'AAYU_OFFICIAL_HANDBOOK.html');
let html = fs.readFileSync(handbookPath, 'utf8');

// 1. Update Chapter 5 with Memory Architecture section
const ch5Old = `<h2>2. Reactive State (<code>state</code>)</h2>
<p>When building full-stack reactive applications or UI components, use <code>state</code>. When a state variable changes, dependent UI elements or routes automatically update:</p>

<pre><code>state count = 0
state user_status = "offline"</code></pre>

<!-- CHAPTER 6 -->`;

const ch5New = `<h2>2. Reactive State (<code>state</code>)</h2>
<p>When building full-stack reactive applications or UI components, use <code>state</code>. When a state variable changes, dependent UI elements or routes automatically update:</p>

<pre><code>state count = 0
state user_status = "offline"</code></pre>

<h2>3. Memory Architecture: Union-Style (NaN-Boxing) &amp; Stack-Style Execution</h2>
<p>Developers frequently ask whether AAYU uses <strong>Union-Style</strong> or <strong>Stack-Style</strong> memory management. The engineering answer is: <strong>AAYU uses an optimized Hybrid Architecture combining Tagged Union (NaN-Boxing) for value representation with high-speed Call-Stack Frames for execution context.</strong></p>

<div class="hinglish">
  <b>Concept Samjhein (Hindi/Hinglish):</b><br>
  AAYU ka memory system do levels par kaam karta hai:<br>
  1. <b>Value Level (Union Style / NaN-Boxing):</b> Har single value (Int, Float, Bool, Null, Heap Pointer) 64-bit word ke andar directly fit hoti hai. Isme C/Python ki tarah alag se boxing ya pointer dereferencing overhead nahi hoti.<br>
  2. <b>Execution Level (Stack Style):</b> Har function call aur local variable stack frame par push hota hai aur function end hote hi <code>O(1)</code> speed me instant pop ho jata hai. Isliye local variables me garbage collector ki zaroorat nahi padti!
</div>

<table>
  <tr>
    <th style="width: 25%;">Memory Layer</th>
    <th style="width: 35%;">Architecture Mechanism</th>
    <th style="width: 40%;">Performance &amp; Silicon Benefit</th>
  </tr>
  <tr>
    <td><strong>Values (Union-Style)</strong></td>
    <td>64-bit NaN-Boxing &amp; Tagged Unions (Int, Float, Bool, Null, Pointer)</td>
    <td>Zero boxing overhead. Primitives fit directly in CPU registers without heap pointer indirection.</td>
  </tr>
  <tr>
    <td><strong>Call Frames (Stack-Style)</strong></td>
    <td>Contiguous LIFO Call-Stack Frames for functions, parameters, and local <code>let</code> bindings</td>
    <td>Instant <code>O(1)</code> push and pop upon function return. Zero garbage collection pauses for function locals.</td>
  </tr>
  <tr>
    <td><strong>Collections (Managed Heap)</strong></td>
    <td>Contiguous Heap Storage for dynamic Arrays (<code>[]</code>), Dictionaries (<code>{}</code>), and Models</td>
    <td>Automated reference tracking and compaction, keeping the total runtime memory footprint at only <strong>2.4 MB RAM</strong>.</td>
  </tr>
</table>

<!-- CHAPTER 6 -->`;

html = html.replace(ch5Old, ch5New);

// 2. Update Chapter 8 with for and while loop details
const ch8Old = `<!-- CHAPTER 8 -->
<h1>Chapter 8: Loops &amp; Iteration</h1>
<p>Loops in AAYU are constructed using <code>while &lt;condition&gt; ... end</code>:</p>

<pre><code>let i = 1
let sum = 0

while i <= 10
    sum = sum + i
    i = i + 1
end

print("Sum of numbers 1 to 10 is:", sum) # 55</code></pre>

<h2>Nested Loops &amp; Matrix Traversal</h2>
<pre><code>let row = 0
while row < 3
    let col = 0
    while col < 3
        print("Cell at [", row, ",", col, "]")
        col = col + 1
    end
    row = row + 1
end</code></pre>

<!-- CHAPTER 9 -->`;

const ch8New = `<!-- CHAPTER 8 -->
<h1>Chapter 8: Loops &amp; Iteration (for &amp; while)</h1>
<p>AAYU provides two first-class iteration constructs: the expressive <code>for &lt;item&gt; in &lt;collection&gt; ... end</code> loop for traversing collections, and the hardware-direct <code>while &lt;condition&gt; ... end</code> loop for condition-driven control flow.</p>

<div class="hinglish">
  <b>Concept Samjhein (Hindi/Hinglish):</b><br>
  AAYU me do tarah ke loops hote hain:<br>
  1. <b><code>for item in list</code></b>: Array ya collection ke har element par traverse karne ke liye sabse clean aur readable syntax.<br>
  2. <b><code>while condition</code></b>: Jab tak condition true hai tab tak loop chalane ke liye (jaise mathematical counting ya matrix operations).
</div>

<h2>1. The Declarative <code>for</code> Loop</h2>
<p>The <code>for</code> loop iterates over arrays and collections without manually managing index variables or boundary checks:</p>

<pre><code>let languages = ["AAYU", "Silicon", "Intent"]

for lang in languages
    print("Core Technology: " + lang)
end</code></pre>

<h3>Summing Numbers with <code>for</code></h3>
<pre><code>let scores = [85, 92, 78, 96, 88]
let total = 0

for s in scores
    total = total + s
end

print("Total Score:", total) # 439</code></pre>

<h2>2. The Condition-Driven <code>while</code> Loop</h2>
<p>For mathematical ranges, counters, or event loops, <code>while &lt;condition&gt; ... end</code> maps directly to hardware branch jumps:</p>

<pre><code>let i = 1
let sum = 0

while i <= 10
    sum = sum + i
    i = i + 1
end

print("Sum of numbers 1 to 10 is:", sum) # 55</code></pre>

<h2>3. Nested Loops &amp; Matrix Traversal</h2>
<pre><code>let row = 0
while row < 3
    let col = 0
    while col < 3
        print("Cell at [", row, ",", col, "]")
        col = col + 1
    end
    row = row + 1
end</code></pre>

<h2>4. How the AAYU Compiler Lowers <code>for</code> (Desugaring)</h2>
<p>Under the hood, AAYU uses <strong>Zero-Overhead Desugaring</strong>. When you write <code>for x in items ... end</code>, the compiler transparently lowers it to an optimized indexed <code>while</code> loop. There are no hidden iterator heap allocations or GC pressure—execution runs at native silicon speed.</p>

<!-- CHAPTER 9 -->`;

html = html.replace(ch8Old, ch8New);

// 3. Update TOC card for Chapter 8
html = html.replace(
  '<div class="toc-chap-title">Loops & Iteration</div>\n    <div class="toc-chap-desc">while ... end, accumulators, infinite loop bounds and guards.</div>',
  '<div class="toc-chap-title">Loops & Iteration (for & while)</div>\n    <div class="toc-chap-desc">for in collection, while condition, accumulators, desugaring.</div>'
);

fs.writeFileSync(handbookPath, html, 'utf8');
console.log('Handbook updated successfully with for loops and memory architecture!');
