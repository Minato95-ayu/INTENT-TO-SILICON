---
layout: home

hero:
  name: "AAYU"
  text: "Architecture-First Programming Platform"
  tagline: "Talk. Design. Generate. Build. From conversation to production software."
  image:
    src: /aayu-logo.png
    alt: AAYU logo
  actions:
    - theme: brand
      text: Get Started
      link: /guide/installation
    - theme: alt
      text: Install
      link: /guide/installation
    - theme: alt
      text: GitHub
      link: https://github.com/Minato95-ayu/INTENT-TO-SILICON

features:
  - title: AAYU Language
    details: Developer Preview
    link: /platform/language
  - title: AAYU Engine
    details: Developer Preview
    link: /platform/engine
  - title: AAYU Studio
    details: Preview
    link: /platform/studio
  - title: AAYU Chat
    details: Experimental
    link: /platform/chat
  - title: BrainOS
    details: Prototype
    link: /platform/brainos
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
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 18px 0 0;
}

.pipeline-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pipeline-step {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 14px 16px;
  background: var(--vp-c-bg-soft);
  font-weight: 650;
  text-align: center;
  flex: 1;
}

.pipeline-arrow {
  color: var(--vp-c-text-2);
  font-weight: 700;
  text-align: center;
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

.builder-note {
  margin-top: 10px;
  font-style: italic;
  color: var(--vp-c-text-2);
  text-align: center;
}
</style>

<section class="aayu-section">
  <h2 style="text-align: center;">Why AAYU? 30 Second Demo</h2>
  <div class="terminal">
    <div><span class="prompt">$</span> aayu chat</div>
    <div>What do you want to build?</div>
    <div><span class="ok">> Hospital Management System</span></div>
    <br>
    <div class="muted">Intent Locked</div>
    <div class="muted">Generated: main.aayu</div>
    <div class="muted">Validating...</div>
    <div class="ok">[OK] Syntax Valid</div>
    <div class="muted">Generating Architecture...</div>
    <div class="ok">[OK] React</div>
    <div class="ok">[OK] FastAPI</div>
    <div class="ok">[OK] PostgreSQL</div>
    <br>
    <div><span class="ok">Project Ready!</span></div>
  </div>
</section>

<section class="aayu-section">
  <h2>Get Started</h2>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
    <div>
      <h3>Track 1: Developers</h3>
      <div class="terminal" style="min-height: 250px;">
        <div><span class="prompt">$</span> git clone https://github.com/Minato95-ayu/INTENT-TO-SILICON.git</div>
        <div><span class="prompt">$</span> pip install -e .</div>
        <div><span class="prompt">$</span> aayu init hospital</div>
        <div><span class="prompt">$</span> aayu generate src/main.aayu</div>
      </div>
    </div>
    <div>
      <h3>Track 2: AI Chat</h3>
      <div class="terminal" style="min-height: 250px;">
        <div><span class="prompt">$</span> aayu chat</div>
        <div class="muted">Answer a few questions</div>
        <div><span class="prompt">></span> Generate? (Y/N) Y</div>
        <div class="ok">Auto-generates main.aayu & Project</div>
      </div>
    </div>
  </div>
</section>

<section class="aayu-section">
  <h2>Centralized Architecture</h2>
  <div class="pipeline">
    <div class="pipeline-step">Developer</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step" style="border-color: #3b82f6;">AAYU Chat</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step" style="border-color: #3b82f6;">Question Engine</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step" style="border-color: #3b82f6;">Intent Engine</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step" style="background: #1e3a8a; color: white;">Builder API</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-step">Parser → Compiler → Generators</div>
    <div class="pipeline-arrow">↓</div>
    <div class="pipeline-row">
      <div class="pipeline-step" style="border-color: #10b981;">React</div>
      <div class="pipeline-step" style="border-color: #10b981;">FastAPI</div>
      <div class="pipeline-step" style="border-color: #10b981;">PostgreSQL</div>
    </div>
  </div>
  <p class="builder-note">
    Builder API is the single integration point used by the CLI, Chat, VS Code Studio, and future web applications.
  </p>
</section>

<section class="aayu-section" style="margin-bottom: 50px;">
  <div style="text-align: center; color: var(--vp-c-text-2);">
    Website v2.0 &mdash; Developer Preview
  </div>
</section>
