import{_ as a,o as e,c as s,a0 as t}from"./chunks/framework.Bogozrur.js";const u=JSON.parse('{"title":"Entity Relations","description":"","frontmatter":{},"headers":[],"relativePath":"web/relations.md","filePath":"web/relations.md"}'),o={name:"web/relations.md"};function p(i,n,l,c,r,d){return e(),s("div",null,[...n[0]||(n[0]=[t(`<h1 id="entity-relations" tabindex="-1">Entity Relations <a class="header-anchor" href="#entity-relations" aria-label="Permalink to &quot;Entity Relations&quot;">​</a></h1><p>In modern applications, entities rarely exist in isolation. AAYU allows you to link entities together natively using the <code>relation</code> keyword, completely removing the need for raw SQL JOINs.</p><p>AAYU automatically configures foreign keys and handles cascading logic at the compiler level.</p><h2 id="one-to-many" tabindex="-1">One-to-Many <a class="header-anchor" href="#one-to-many" aria-label="Permalink to &quot;One-to-Many&quot;">​</a></h2><p>The most common relationship. For example, a single <code>Doctor</code> can have multiple <code>Appointment</code>s.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>use db.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>entity Doctor.</span></span>
<span class="line"><span>    text name.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>entity Appointment.</span></span>
<span class="line"><span>    text date.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># AAYU handles the foreign key injection automatically</span></span>
<span class="line"><span>relation Doctor one_to_many Appointment.</span></span></code></pre></div><h2 id="many-to-many" tabindex="-1">Many-to-Many <a class="header-anchor" href="#many-to-many" aria-label="Permalink to &quot;Many-to-Many&quot;">​</a></h2><p>For complex systems, such as a Learning Management System where a <code>Student</code> can enroll in multiple <code>Course</code>s, and a <code>Course</code> can have multiple <code>Student</code>s.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>entity Student.</span></span>
<span class="line"><span>    text name.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>entity Course.</span></span>
<span class="line"><span>    text title.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span># AAYU handles the underlying junction architecture natively</span></span>
<span class="line"><span>relation Student many_to_many Course.</span></span></code></pre></div><h2 id="supported-relation-types" tabindex="-1">Supported Relation Types <a class="header-anchor" href="#supported-relation-types" aria-label="Permalink to &quot;Supported Relation Types&quot;">​</a></h2><ul><li><code>one_to_one</code></li><li><code>one_to_many</code></li><li><code>many_to_one</code></li><li><code>many_to_many</code></li></ul><p>By defining these relations natively, AAYU&#39;s Intent Engine is able to construct deep, generalized business systems instantly.</p>`,12)])])}const h=a(o,[["render",p]]);export{u as __pageData,h as default};
