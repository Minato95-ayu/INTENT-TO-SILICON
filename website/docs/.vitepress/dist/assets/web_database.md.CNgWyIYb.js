import{_ as s,o as n,c as e,a0 as t}from"./chunks/framework.Bogozrur.js";const u=JSON.parse('{"title":"Database Models","description":"","frontmatter":{},"headers":[],"relativePath":"web/database.md","filePath":"web/database.md"}'),p={name:"web/database.md"};function l(i,a,o,d,c,r){return n(),e("div",null,[...a[0]||(a[0]=[t(`<h1 id="database-models" tabindex="-1">Database Models <a class="header-anchor" href="#database-models" aria-label="Permalink to &quot;Database Models&quot;">​</a></h1><p>AAYU abstracts the database layer so you can define tables naturally. The default database engine is SQLite.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use db.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>entity Book.</span></span>
<span class="line"><span>    text title.</span></span>
<span class="line"><span>    text author.</span></span>
<span class="line"><span>    number year_published.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># Querying the database</span></span>
<span class="line"><span>task get_books.</span></span>
<span class="line"><span>    return db_find(&quot;Book&quot;, {}).</span></span>
<span class="line"><span>end.</span></span></code></pre></div>`,3)])])}const _=s(p,[["render",l]]);export{u as __pageData,_ as default};
