"""
=============================================================================
FILE: generator.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

import os
import string
from generators.base import BaseGenerator

class ReactGenerator(BaseGenerator):
    def __init__(self, ir_data: dict, output_dir: str):
        super().__init__(ir_data, output_dir)
        self.tpl_dir = os.path.join(os.path.dirname(__file__), "templates")

    def _read_tpl(self, name: str) -> str:
        with open(os.path.join(self.tpl_dir, name), "r", encoding="utf-8") as f:
            return f.read()

    def generate(self):
        print(f"Generating React App in {self.output_dir}...")
        
        app_name = self.ir.get("system", {}).get("name", "AAYU_App")
        pages = self.ir.get("pages", [])
        
        # If no pages are defined but UI feature is present, or just as fallback:
        if not pages:
            pages = [{"name": "Home"}]
            
        # 1. Static Files
        self.write_file("package.json", self._read_tpl("package.json.tpl"))
        self.write_file("vite.config.js", self._read_tpl("vite.config.js.tpl"))
        self.write_file("tailwind.config.js", self._read_tpl("tailwind.config.js.tpl"))
        self.write_file("postcss.config.js", self._read_tpl("postcss.config.js.tpl"))
        self.write_file("src/index.css", self._read_tpl("index.css.tpl"))
        self.write_file("src/main.jsx", self._read_tpl("main.jsx.tpl"))

        # 2. index.html
        html_tpl = string.Template(self._read_tpl("index.html.tpl"))
        self.write_file("index.html", html_tpl.substitute(app_name=app_name))

        # 3. Pages
        page_tpl = string.Template(self._read_tpl("Page.jsx.tpl"))
        for page in pages:
            page_name = page["name"]
            content = page_tpl.substitute(page_name=page_name)
            self.write_file(f"src/pages/{page_name}.jsx", content)

        # 4. App.jsx
        app_tpl = string.Template(self._read_tpl("App.jsx.tpl"))
        
        imports = []
        nav_links = []
        routes = []
        
        for i, page in enumerate(pages):
            page_name = page["name"]
            path = "/" if i == 0 else f"/{page_name.lower()}"
            
            imports.append(f"import {page_name} from './pages/{page_name}'")
            nav_links.append(f'              <Link to="{path}" className="hover:text-indigo-200 transition">{page_name}</Link>')
            routes.append(f'            <Route path="{path}" element={{<{page_name} />}} />')
            
        app_content = app_tpl.substitute(
            app_name=app_name,
            page_imports="\n".join(imports),
            nav_links="\n".join(nav_links),
            routes="\n".join(routes)
        )
        self.write_file("src/App.jsx", app_content)

        print("React generation complete.")
