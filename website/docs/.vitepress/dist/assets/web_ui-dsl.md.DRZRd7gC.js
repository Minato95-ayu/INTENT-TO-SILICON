import{_ as n,o as s,c as e,a0 as t}from"./chunks/framework.bcCluOOn.js";const h=JSON.parse('{"title":"UI DSL","description":"","frontmatter":{},"headers":[],"relativePath":"web/ui-dsl.md","filePath":"web/ui-dsl.md"}'),p={name:"web/ui-dsl.md"};function i(o,a,l,c,d,r){return s(),e("div",null,[...a[0]||(a[0]=[t(`<h1 id="ui-dsl" tabindex="-1">UI DSL <a class="header-anchor" href="#ui-dsl" aria-label="Permalink to &quot;UI DSL&quot;">​</a></h1><p>AAYU is not just a backend architecture language. It possesses a full <strong>UI Domain Specific Language (DSL)</strong> capable of rendering visual frontends directly from the <code>.aayu</code> syntax.</p><h2 id="pages-and-components" tabindex="-1">Pages and Components <a class="header-anchor" href="#pages-and-components" aria-label="Permalink to &quot;Pages and Components&quot;">​</a></h2><p>You can define standard UI screens using the <code>page</code> keyword. Inside a page, you can nest layout components seamlessly.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>page Dashboard.</span></span>
<span class="line"><span>    </span></span>
<span class="line"><span>    card.</span></span>
<span class="line"><span>        heading &quot;Welcome to Hospital Admin&quot;.</span></span>
<span class="line"><span>        text &quot;Manage all your patients easily.&quot;</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span>    </span></span>
<span class="line"><span>    card.</span></span>
<span class="line"><span>        button &quot;View Patients&quot;.</span></span>
<span class="line"><span>        button &quot;Book Appointment&quot;.</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>end.</span></span></code></pre></div><p>When you compile an AAYU file containing a <code>page</code>, the internal Compiler synthesizes actual, styled <code>HTML/CSS</code> representations into your <code>views/</code> directory dynamically.</p><h2 id="integrating-ui-with-server" tabindex="-1">Integrating UI with Server <a class="header-anchor" href="#integrating-ui-with-server" aria-label="Permalink to &quot;Integrating UI with Server&quot;">​</a></h2><p>You can map a UI page directly to an HTTP GET route using the <code>render</code> command.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use http.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>get &quot;/dashboard&quot;.</span></span>
<span class="line"><span>    render &quot;Dashboard&quot;.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>task main.</span></span>
<span class="line"><span>    serve on 8080.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><p>Combined with the <code>crud Entity.</code> command, AAYU dynamically generates fully functional data-tables and submission forms in real-time, removing the requirement to write hundreds of lines of React/Vue frontend logic just to see your database values.</p>`,10)])])}const g=n(p,[["render",i]]);export{h as __pageData,g as default};
