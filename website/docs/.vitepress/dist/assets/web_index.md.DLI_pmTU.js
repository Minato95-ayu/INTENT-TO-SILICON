import{_ as a,o as s,c as e,a0 as p}from"./chunks/framework.Bogozrur.js";const h=JSON.parse('{"title":"Web Development","description":"","frontmatter":{},"headers":[],"relativePath":"web/index.md","filePath":"web/index.md"}'),t={name:"web/index.md"};function i(l,n,o,c,d,r){return s(),e("div",null,[...n[0]||(n[0]=[p(`<h1 id="web-development" tabindex="-1">Web Development <a class="header-anchor" href="#web-development" aria-label="Permalink to &quot;Web Development&quot;">​</a></h1><p>AAYU eliminates the boundary between backend and frontend. The language natively understands web concepts like routing, requests, views, and server states.</p><h2 id="the-http-module" tabindex="-1">The HTTP Module <a class="header-anchor" href="#the-http-module" aria-label="Permalink to &quot;The HTTP Module&quot;">​</a></h2><p>By invoking the <code>use http.</code> module, AAYU unlocks its internal HTTP server engine.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use http.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>task main.</span></span>
<span class="line"><span>    serve on 8080.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><p>The <code>serve on 8080.</code> command binds AAYU to the given port and begins accepting requests natively. AAYU&#39;s VM spins up isolated, thread-safe Sub-VM instances for every incoming request, ensuring zero variable leaking between web sessions.</p><h2 id="custom-routing" tabindex="-1">Custom Routing <a class="header-anchor" href="#custom-routing" aria-label="Permalink to &quot;Custom Routing&quot;">​</a></h2><p>You can declare specific REST routes natively without any framework boilerplate.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use http.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>get &quot;/hello&quot;.</span></span>
<span class="line"><span>    print &quot;Handling GET request&quot;.</span></span>
<span class="line"><span>    render &quot;home&quot;.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>post &quot;/submit&quot;.</span></span>
<span class="line"><span>    text name.</span></span>
<span class="line"><span>    get_form &quot;name&quot; into name.</span></span>
<span class="line"><span>    print name.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>task main.</span></span>
<span class="line"><span>    serve on 8080.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><h2 id="auto-crud-generation" tabindex="-1">Auto-CRUD Generation <a class="header-anchor" href="#auto-crud-generation" aria-label="Permalink to &quot;Auto-CRUD Generation&quot;">​</a></h2><p>Writing repetitive Create, Read, Update, Delete routes is a thing of the past. If you declare an Entity, AAYU can auto-generate the complete backend routes and frontend UI screens for it using a single line of code.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use http.</span></span>
<span class="line"><span>use db.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>entity Student.</span></span>
<span class="line"><span>    text name.</span></span>
<span class="line"><span>    number age.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># This single line generates the REST APIs and UI Admin panel!</span></span>
<span class="line"><span>crud Student.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>task main.</span></span>
<span class="line"><span>    serve on 8080.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><p>Navigate to <code>/student</code> on your browser, and you will see a fully functioning, styled dashboard to manage <code>Student</code> records!</p>`,13)])])}const m=a(t,[["render",i]]);export{h as __pageData,m as default};
