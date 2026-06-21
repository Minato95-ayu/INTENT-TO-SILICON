import{_ as n,o as s,c as e,a0 as t}from"./chunks/framework.Bogozrur.js";const h=JSON.parse('{"title":"Routing and Views","description":"","frontmatter":{},"headers":[],"relativePath":"web/routing.md","filePath":"web/routing.md"}'),p={name:"web/routing.md"};function i(o,a,l,r,c,d){return s(),e("div",null,[...a[0]||(a[0]=[t(`<h1 id="routing-and-views" tabindex="-1">Routing and Views <a class="header-anchor" href="#routing-and-views" aria-label="Permalink to &quot;Routing and Views&quot;">​</a></h1><p>AAYU has a built-in web server. You don&#39;t need any complex frameworks to start a web application.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use http.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>task handle_home with req.</span></span>
<span class="line"><span>    return render &quot;home.html&quot;.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>route &quot;/&quot; to handle_home.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>serve on 8080.</span></span></code></pre></div>`,3)])])}const _=n(p,[["render",i]]);export{h as __pageData,_ as default};
