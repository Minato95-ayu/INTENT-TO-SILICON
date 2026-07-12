import os
import json
from typing import Dict, Any

class ReactGenerator:
    """
    Consumes App IR and generates a React Vite application.
    """
    def __init__(self, ir: Dict[str, Any], output_dir: str = "react_app"):
        self.ir = ir
        self.output_dir = output_dir

    def generate(self):
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src"), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, "src", "pages"), exist_ok=True)
        
        project_name = self.ir.get("project", "aayu-react-app").lower().replace(" ", "-")
        
        # package.json
        pkg_json = {
            "name": project_name,
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "tsc -b && vite build",
                "lint": "eslint .",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.3.1",
                "react-dom": "^18.3.1",
                "react-router-dom": "^6.26.1"
            },
            "devDependencies": {
                "@types/react": "^18.3.3",
                "@types/react-dom": "^18.3.0",
                "@vitejs/plugin-react": "^4.3.1",
                "typescript": "^5.5.3",
                "vite": "^5.4.1"
            }
        }
        
        with open(os.path.join(self.output_dir, "package.json"), "w", encoding="utf-8") as f:
            json.dump(pkg_json, f, indent=2)
            
        # vite.config.ts
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
"""
        with open(os.path.join(self.output_dir, "vite.config.ts"), "w", encoding="utf-8") as f:
            f.write(vite_config)
            
        # tsconfig.json
        tsconfig = {
          "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": True,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": True,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": True,
            "resolveJsonModule": True,
            "isolatedModules": True,
            "noEmit": True,
            "jsx": "react-jsx",
            "strict": True,
            "noUnusedLocals": False,
            "noUnusedParameters": False,
            "noFallthroughCasesInSwitch": True
          },
          "include": ["src"]
        }
        with open(os.path.join(self.output_dir, "tsconfig.json"), "w", encoding="utf-8") as f:
            json.dump(tsconfig, f, indent=2)

        # index.html
        index_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{self.ir.get('project', 'React App')}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""
        with open(os.path.join(self.output_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

        # src/main.tsx
        main_tsx = """import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.tsx'
import './index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
"""
        with open(os.path.join(self.output_dir, "src", "main.tsx"), "w", encoding="utf-8") as f:
            f.write(main_tsx)

        # src/index.css
        css_content = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
.aayu-flex { display: flex; }
.aayu-stack { display: flex; flex-direction: column; }
.aayu-center { align-items: center; justify-content: center; }
.aayu-spacer { flex-grow: 1; }
"""
        # Inject Theme
        ui_ir = self.ir.get("ui_ir", {})
        themes = ui_ir.get("themes", [])
        theme = themes[0] if themes else None
        if theme:
            css_content += ":root {\n"
            for k, v in theme.get("properties", {}).items():
                css_content += f"  --{k}: {v};\n"
            css_content += "}\n"
        
        with open(os.path.join(self.output_dir, "src", "index.css"), "w", encoding="utf-8") as f:
            f.write(css_content)

        # Generate Pages
        ui_tree = ui_ir.get("pages", [])
        page_names = []
        for page in ui_tree:
            page_name = page["name"]
            page_names.append(page_name)
            self._generate_page(page, os.path.join(self.output_dir, "src", "pages", f"{page_name}.tsx"))

        # src/App.tsx
        routes = ui_ir.get("routes", [])
        app_tsx_lines = [
            "import { Routes, Route } from 'react-router-dom';"
        ]
        for name in page_names:
            app_tsx_lines.append(f"import {name} from './pages/{name}';")
            
        app_tsx_lines.extend([
            "",
            "function App() {",
            "  return (",
            "    <Routes>"
        ])
        
        if not routes and page_names:
            # Default single page route
            app_tsx_lines.append(f"      <Route path='/' element={{<{page_names[0]} />}} />")
        else:
            for route in routes:
                app_tsx_lines.append(f"      <Route path='{route['path']}' element={{<{route['target_page']} />}} />")

        app_tsx_lines.extend([
            "    </Routes>",
            "  )",
            "}",
            "",
            "export default App;"
        ])
        
        with open(os.path.join(self.output_dir, "src", "App.tsx"), "w", encoding="utf-8") as f:
            f.write("\n".join(app_tsx_lines))
            
        print(f"[React Generator] Generated project '{project_name}' in '{self.output_dir}'")

    def _generate_page(self, page_ir: Dict[str, Any], filepath: str):
        lines = []
        state_tree = self.ir.get("ui_ir", {}).get("state", [])
        if state_tree:
            lines.append("import { useState } from 'react';")
        lines.append(f"export default function {page_ir['name']}() {{")
        
        for state in state_tree:
            lines.append(f"  const [{state['name']}, set{state['name'].capitalize()}] = useState({state['initial_value']});")
            
        lines.append("  return (")
        lines.append("    <div className='page'>")
        
        for child in page_ir.get("children", []):
            lines.extend(self._generate_component(child, indent=6))
            
        lines.append("    </div>")
        lines.append("  )")
        lines.append("}")
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _generate_component(self, comp: Dict[str, Any], indent: int) -> list:
        spaces = " " * indent
        lines = []
        ctype = comp.get("type")
        props = comp.get("properties", {})
        
        # Build style and className
        style_parts = []
        classes = []
        event_handlers = []
        inner_text = ""
        
        if ctype == "stack" or ctype == "column":
            classes.append("aayu-stack")
        elif ctype == "row" or ctype == "flex":
            classes.append("aayu-flex")
            
        for k, v in props.items():
            if k == "text":
                inner_text = v
            elif k == "padding":
                style_parts.append(f"padding: {v}")
            elif k == "center":
                classes.append("aayu-center")
            elif k == "color" or k == "background":
                style_parts.append(f"{k}: 'var(--{v})'")
            elif k.startswith("on_"):
                # React event handlers expect a function
                event_handlers.append(f"onClick={{() => {{ {v} }}}}")
            elif isinstance(v, dict) and "__bind__" in v:
                inner_text = f"{{{v['__bind__']}}}"
                
        style_str = f" style={{{{ {', '.join(style_parts)} }}}}" if style_parts else ""
        class_str = f" className='{' '.join(classes)}'" if classes else ""
        events_str = " " + " ".join(event_handlers) if event_handlers else ""
        
        if ctype == "button":
            lines.append(f"{spaces}<button{class_str}{style_str}{events_str}>{inner_text}</button>")
        elif ctype == "heading":
            lines.append(f"{spaces}<h1{class_str}{style_str}{events_str}>{inner_text}</h1>")
        elif ctype == "text":
            lines.append(f"{spaces}<p{class_str}{style_str}{events_str}>{inner_text}</p>")
        else:
            lines.append(f"{spaces}<div{class_str}{style_str}{events_str}>")
            if inner_text:
                lines.append(f"{spaces}  {inner_text}")
            for child in comp.get("children", []):
                lines.extend(self._generate_component(child, indent + 2))
            lines.append(f"{spaces}</div>")
            
        return lines
