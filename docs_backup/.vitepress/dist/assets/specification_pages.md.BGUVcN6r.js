import{_ as n,o as e,c as s,a0 as t}from"./chunks/framework.bcCluOOn.js";const h=JSON.parse('{"title":"Pages & UI DSL","description":"","frontmatter":{},"headers":[],"relativePath":"specification/pages.md","filePath":"specification/pages.md"}'),p={name:"specification/pages.md"};function o(i,a,l,d,c,r){return e(),s("div",null,[...a[0]||(a[0]=[t(`<h1 id="pages-ui-dsl" tabindex="-1">Pages &amp; UI DSL <a class="header-anchor" href="#pages-ui-dsl" aria-label="Permalink to &quot;Pages &amp; UI DSL&quot;">​</a></h1><p>A core feature of the AAYU platform is its ability to not just generate backend APIs, but full-stack applications. To achieve this, AAYU includes a declarative Domain-Specific Language (DSL) for defining user interfaces.</p><p>The UI DSL allows developers to outline the structure and components of a frontend without writing HTML, CSS, or React directly.</p><h2 id="the-page-block" tabindex="-1">The <code>page</code> Block <a class="header-anchor" href="#the-page-block" aria-label="Permalink to &quot;The \`page\` Block&quot;">​</a></h2><p>A UI view is defined using the <code>page</code> keyword.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>page LoginView.</span></span>
<span class="line"><span>    heading &quot;Welcome to AAYU&quot;.</span></span>
<span class="line"><span>    button &quot;Login&quot;.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><h2 id="layout-components" tabindex="-1">Layout Components <a class="header-anchor" href="#layout-components" aria-label="Permalink to &quot;Layout Components&quot;">​</a></h2><p>AAYU provides semantic layout components to structure the page.</p><h3 id="dashboard" tabindex="-1"><code>dashboard</code> <a class="header-anchor" href="#dashboard" aria-label="Permalink to &quot;\`dashboard\`&quot;">​</a></h3><p>The <code>dashboard</code> component automatically provisions a standard administrative layout (typically a sidebar on the left and a main content area on the right).</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>page AdminArea.</span></span>
<span class="line"><span>    dashboard.</span></span>
<span class="line"><span>        # Sidebar goes here</span></span>
<span class="line"><span>        # Main content goes here</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><h3 id="sidebar-and-column" tabindex="-1"><code>sidebar</code> and <code>column</code> <a class="header-anchor" href="#sidebar-and-column" aria-label="Permalink to &quot;\`sidebar\` and \`column\`&quot;">​</a></h3><p>Used within a <code>dashboard</code> or page to organize content vertically.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>page CRM.</span></span>
<span class="line"><span>    dashboard.</span></span>
<span class="line"><span>        sidebar.</span></span>
<span class="line"><span>            text &quot;Leads&quot;.</span></span>
<span class="line"><span>            text &quot;Customers&quot;.</span></span>
<span class="line"><span>            text &quot;Settings&quot;.</span></span>
<span class="line"><span>        end.</span></span>
<span class="line"><span>        column.</span></span>
<span class="line"><span>            heading &quot;Dashboard Overview&quot;.</span></span>
<span class="line"><span>            text &quot;Welcome back, Admin.&quot;.</span></span>
<span class="line"><span>        end.</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><h2 id="data-integration-components" tabindex="-1">Data Integration Components <a class="header-anchor" href="#data-integration-components" aria-label="Permalink to &quot;Data Integration Components&quot;">​</a></h2><h3 id="table" tabindex="-1"><code>table</code> <a class="header-anchor" href="#table" aria-label="Permalink to &quot;\`table\`&quot;">​</a></h3><p>The <code>table</code> component seamlessly integrates with AAYU <code>entity</code> definitions to automatically generate data grids.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>entity Patient.</span></span>
<span class="line"><span>    text name.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>page PatientList.</span></span>
<span class="line"><span>    column.</span></span>
<span class="line"><span>        heading &quot;All Patients&quot;.</span></span>
<span class="line"><span>        table &quot;Patients&quot; from Patient.</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><p><em>Compiler Action:</em> The compiler will generate the necessary frontend code (e.g., a React component) to fetch <code>Patient</code> data from the backend and render it in a tabular format.</p><h3 id="form-and-input" tabindex="-1"><code>form</code> and <code>input</code> <a class="header-anchor" href="#form-and-input" aria-label="Permalink to &quot;\`form\` and \`input\`&quot;">​</a></h3><p>Used to capture user input.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>page AddLead.</span></span>
<span class="line"><span>    form.</span></span>
<span class="line"><span>        input &quot;Company Name&quot; to lead_company.</span></span>
<span class="line"><span>        input &quot;Contact Email&quot; to lead_email.</span></span>
<span class="line"><span>        button &quot;Save Lead&quot;.</span></span>
<span class="line"><span>    end.</span></span>
<span class="line"><span>end.</span></span></code></pre></div><h2 id="rendering-pages" tabindex="-1">Rendering Pages <a class="header-anchor" href="#rendering-pages" aria-label="Permalink to &quot;Rendering Pages&quot;">​</a></h2><p>Pages are rendered from within <code>task</code> blocks (route handlers) using the <code>render</code> keyword.</p><div class="language-aayu vp-adaptive-theme"><button title="Copy Code" class="copy"></button><span class="lang">aayu</span><pre class="shiki shiki-themes github-light github-dark vp-code" tabindex="0"><code><span class="line"><span>task show_dashboard with req.</span></span>
<span class="line"><span>    return render &quot;CRM.html&quot;.</span></span>
<span class="line"><span>end.</span></span>
<span class="line"><span></span></span>
<span class="line"><span>get &quot;/dashboard&quot; to show_dashboard.</span></span></code></pre></div><p><em>(Note: Current prototype targets generate <code>.html</code> strings natively. Future Target Generators will emit React/Vue router code based on these declarations).</em></p>`,26)])])}const g=n(p,[["render",o]]);export{h as __pageData,g as default};
