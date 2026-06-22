---
layout: home

hero:
  name: "AAYU"
  text: "v1.0 Developer Preview"
  tagline: "Architecture-First Software Factory"
  image:
    src: /aayu-logo.png
    alt: AAYU logo
  actions:
    - theme: brand
      text: Get Started
      link: /guide/installation
    - theme: alt
      text: Language Guide
      link: /guide/syntax
    - theme: alt
      text: Runtime Status
      link: /specification/runtime

features:
  - title: Business Intent or AAYU Code
    details: Start from a plain business requirement or a direct .aayu source file.
  - title: Compiler to Architecture
    details: AAYU parses source, builds IR, selects targets, and generates full-stack software.
  - title: Experimental Runtime
    details: Sprint 35 verifies AAYU Source -> Parser -> Compiler -> AYC -> VM -> Execution.
---

<style>
.aayu-section {
  margin-top: 56px;
}

.aayu-section h2 {
  margin-bottom: 18px;
  font-size: 1.65rem;
}

.pipeline {
  display: grid;
  gap: 12px;
  margin: 18px 0 0;
}

.pipeline-step {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 14px 16px;
  background: var(--vp-c-bg-soft);
  font-weight: 650;
}

.pipeline-arrow {
  color: var(--vp-c-text-2);
  font-weight: 700;
  padding-left: 16px;
}

.terminal {
  overflow-x: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 20px;
  background: #111827;
  color: #e5e7eb;
  font-family: ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace;
  line-height: 1.7;
}

.prompt {
  color: #7dd3fc;
}

.ok {
  color: #86efac;
}

.muted {
  color: #9ca3af;
}

.status-grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
}

.status-panel {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 18px;
  background: var(--vp-c-bg-soft);
}

.bar {
  height: 12px;
  margin: 12px 0;
  border-radius: 999px;
  background: var(--vp-c-divider);
  overflow: hidden;
}

.fill-a {
  width: 100%;
  height: 100%;
  background: #0f8a78;
}

.fill-b {
  width: 40%;
  height: 100%;
  background: #1464f6;
}
</style>

<section class="aayu-section">
  <h2>Verified Generation Flow</h2>
  <div class="pipeline">
    <div class="pipeline-step">Business Intent OR AAYU Code</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">AAYU Language</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">AAYU Compiler</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">AAYU IR</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">Target Selection Engine</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">React + FastAPI + PostgreSQL</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">Production-Ready Software</div>
  </div>
</section>

<section class="aayu-section">
  <h2>Install and Generate</h2>
  <div class="terminal">
    <div><span class="prompt">$</span> pip install aayu</div>
    <div><span class="prompt">$</span> aayu init hospital</div>
    <div><span class="prompt">$</span> aayu generate src/main.aayu</div>
    <br>
    <div class="ok">generated/</div>
    <div class="muted">|-- frontend/</div>
    <div class="muted">|-- backend/</div>
    <div class="muted">|-- database/</div>
    <div class="muted">`-- docker-compose.yml</div>
  </div>
</section>

<section class="aayu-section">
  <h2>Runtime Roadmap</h2>
  <div class="pipeline">
    <div class="pipeline-step">AAYU Code</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">AYC Bytecode</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">AAYU Runtime (Rust)</div>
    <div class="pipeline-arrow">down</div>
    <div class="pipeline-step">Execution</div>
  </div>
</section>

<section class="aayu-section">
  <h2>Current Maturity</h2>
  <div class="status-grid">
    <div class="status-panel">
      <strong>Track A: Software Factory</strong>
      <div class="bar"><div class="fill-a"></div></div>
      <span>100% developer preview capability.</span>
    </div>
    <div class="status-panel">
      <strong>Track B: Experimental Runtime</strong>
      <div class="bar"><div class="fill-b"></div></div>
      <span>40% foundation. Variables, print, and if are verified through Sprint 35.</span>
    </div>
  </div>
</section>

<section class="aayu-section">
  <h2>Sprint 35 Verification</h2>
  <div class="terminal">
    <div><span class="prompt">$</span> python -m prototype.cli vm prototype/tests/demo_sprint35.aayu</div>
    <br>
    <div class="ok">Founder</div>
  </div>
</section>
