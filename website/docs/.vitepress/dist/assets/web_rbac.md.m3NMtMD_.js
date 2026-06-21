import{_ as s,o as n,c as e,a0 as i}from"./chunks/framework.Bogozrur.js";const u=JSON.parse('{"title":"Role-Based Access Control (RBAC)","description":"","frontmatter":{},"headers":[],"relativePath":"web/rbac.md","filePath":"web/rbac.md"}'),p={name:"web/rbac.md"};function t(l,a,o,r,c,d){return n(),e("div",null,[...a[0]||(a[0]=[i(`<h1 id="role-based-access-control-rbac" tabindex="-1">Role-Based Access Control (RBAC) <a class="header-anchor" href="#role-based-access-control-rbac" aria-label="Permalink to &quot;Role-Based Access Control (RBAC)&quot;">​</a></h1><p>In traditional frameworks, handling authentication, sessions, and route guards requires heavy middleware and third-party libraries like JWT or Passport.</p><p>AAYU eliminates this by baking <strong>Session Management</strong> and <strong>RBAC</strong> directly into the core grammar.</p><h2 id="defining-roles" tabindex="-1">Defining Roles <a class="header-anchor" href="#defining-roles" aria-label="Permalink to &quot;Defining Roles&quot;">​</a></h2><p>You can define user roles natively using the <code>role</code> keyword.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use rbac.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>role Admin.</span></span>
<span class="line"><span>role Doctor.</span></span>
<span class="line"><span>role Patient.</span></span></code></pre></div><h2 id="assigning-permissions" tabindex="-1">Assigning Permissions <a class="header-anchor" href="#assigning-permissions" aria-label="Permalink to &quot;Assigning Permissions&quot;">​</a></h2><p>Once roles are defined, you can assign explicit CRUD permissions to them via the <code>allow</code> keyword.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>entity Prescription.</span></span>
<span class="line"><span>    text medication.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># Only the Doctor can create a Prescription</span></span>
<span class="line"><span>allow Doctor create Prescription.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># A Patient can read a Prescription</span></span>
<span class="line"><span>allow Patient read Prescription.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># An Admin can do everything</span></span>
<span class="line"><span>allow Admin read Prescription.</span></span>
<span class="line"><span>allow Admin delete Prescription.</span></span></code></pre></div><h2 id="guarding-web-routes" tabindex="-1">Guarding Web Routes <a class="header-anchor" href="#guarding-web-routes" aria-label="Permalink to &quot;Guarding Web Routes&quot;">​</a></h2><p>When writing custom HTTP routes, you can enforce strict session requirements natively.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use auth.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>get &quot;/dashboard&quot;.</span></span>
<span class="line"><span>    # This acts as a native middleware. If the user is not logged in, </span></span>
<span class="line"><span>    # it immediately halts execution and returns a 401 Unauthorized.</span></span>
<span class="line"><span>    guard session.</span></span>
<span class="line"><span>    </span></span>
<span class="line"><span>    render &quot;Dashboard&quot;.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><p>The AAYU compiler handles the underlying cryptography (PBKDF2 hashing) and state isolation entirely automatically.</p>`,13)])])}const g=s(p,[["render",t]]);export{u as __pageData,g as default};
