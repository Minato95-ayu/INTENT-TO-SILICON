---
layout: home

hero:
  name: "AAYU"
  text: "Intent to Application Platform"
  tagline: "The world's first Intent Operating System"
  actions:
    - theme: brand
      text: Get Started
      link: /guide/installation
    - theme: alt
      text: View Documentation
      link: /guide/syntax

features:
  - title: Install Natively
    details: pip install aayu-lang
  - title: Intent Engine v4
    details: Build complex enterprise applications natively by just typing a sentence.
  - title: Zero Boilerplate
    details: Web server, database, authentication, RBAC, and UI built directly into the language syntax.
---

<style>
:root {
  --vp-c-brand-1: #6E56CF;
  --vp-c-brand-2: #8974e6;
  --vp-c-brand-3: #5840b5;
}
.demo-box {
  background: #111111;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 2rem;
  color: #fff;
  font-family: 'JetBrains Mono', monospace;
  margin-top: 4rem;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.5);
}
.demo-title {
  text-align: center;
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 2rem;
  color: var(--vp-c-brand-1);
}
.command { color: #4ade80; font-weight: bold; }
.output { color: #9ca3af; margin-top: 1rem; line-height: 1.6; }
.check { color: #3b82f6; font-weight: bold; }
</style>

<div class="demo-box">
  <div class="demo-title">Build a Full-Stack App in 10 Seconds</div>
  <div class="command">$ aayu build "Build a Hospital Management System"</div>
  <div class="output">
    --- AAYU Intent Engine v4 ---<br>
    [*] Parsing Intent: 'Build a Hospital Management System'<br>
    [*] Inferred Domain: Hospital<br><br>
    <span class="check">✓</span> Roles Generated (Admin, Doctor, Patient)<br>
    <span class="check">✓</span> Entities Generated (Patient, Appointment, Prescription)<br>
    <span class="check">✓</span> Relations Generated (1:N, M:N)<br>
    <span class="check">✓</span> Workflow Generated (AppointmentWorkflow)<br>
    <span class="check">✓</span> UI Generated (Dashboard, CRUD)<br>
    <span class="check">✓</span> Database Configured<br><br>
    <span style="color: #4ade80; font-weight: bold;">[SUCCESS] Generated main.aayu!</span><br>
    Run `aayu run` to start the server.
  </div>
</div>
