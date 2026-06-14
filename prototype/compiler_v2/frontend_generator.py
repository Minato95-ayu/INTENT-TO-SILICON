"""
Aayu Frontend Generator

Generates a React + Vite application driven strictly by the OpenAPI Spec.
No AST, no SchemaModel. Just OpenAPI.
"""
import json
from typing import Dict, List, Set

class FrontendGenerator:
    def __init__(self):
        pass

    def _to_pascal_case(self, text: str) -> str:
        return "".join(x.title() for x in text.replace("-", "_").split("_"))

    def _extract_entities(self, openapi_spec: dict) -> List[str]:
        entities = set()
        paths = openapi_spec.get("paths", {})
        for path in paths.keys():
            # e.g., "/patient" or "/patient/{item_id}"
            parts = [p for p in path.split("/") if p]
            if len(parts) > 0 and not parts[0].startswith("{"):
                entities.add(parts[0])
        return sorted(list(entities))

    def _get_schema_properties(self, openapi_spec: dict, entity: str) -> Dict[str, dict]:
        pascal_entity = self._to_pascal_case(entity)
        schemas = openapi_spec.get("components", {}).get("schemas", {})
        # Look for {Entity}Create schema to know what fields to show in the form
        schema_name = f"{pascal_entity}Create"
        if schema_name in schemas:
            return schemas[schema_name].get("properties", {})
        return {}

    def generate(self, openapi_spec: dict) -> Dict[str, str]:
        files = {}
        entities = self._extract_entities(openapi_spec)
        
        # 1. Base Project Files
        files["package.json"] = self._gen_package_json()
        files["vite.config.ts"] = self._gen_vite_config()
        files["tsconfig.json"] = self._gen_tsconfig()
        files["index.html"] = self._gen_index_html()
        files["src/main.tsx"] = self._gen_main_tsx()
        files["src/services/api.ts"] = self._gen_api_service()
        
        # 2. Entity Pages
        for entity in entities:
            pascal = self._to_pascal_case(entity)
            props = self._get_schema_properties(openapi_spec, entity)
            files[f"src/pages/{pascal}List.tsx"] = self._gen_entity_list(entity, pascal, props)
            files[f"src/pages/{pascal}Form.tsx"] = self._gen_entity_form(entity, pascal, props)
            
        # 3. App Routing
        files["src/App.tsx"] = self._gen_app_tsx(entities)
        
        return files

    def _gen_package_json(self) -> str:
        return """{
  "name": "aayu-generated-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "axios": "^1.6.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.2.2",
    "vite": "^5.0.0"
  }
}
"""

    def _gen_vite_config(self) -> str:
        return """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
"""

    def _gen_tsconfig(self) -> str:
        return """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": false,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": false
  },
  "include": ["src"]
}
"""

    def _gen_index_html(self) -> str:
        return """<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Aayu App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

    def _gen_main_tsx(self) -> str:
        return """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

    def _gen_api_service(self) -> str:
        return """import axios from 'axios';

// Ensure this matches your FastAPI backend URL
export const api = axios.create({
  baseURL: 'http://localhost:8000',
});
"""

    def _gen_entity_list(self, entity: str, pascal: str, props: dict) -> str:
        # Display ID and the first string field if available
        display_col = "id"
        for p_name, p_val in props.items():
            if p_name != "id":
                display_col = p_name
                break
                
        return f"""import React, {{ useEffect, useState }} from 'react';
import {{ Link }} from 'react-router-dom';
import {{ api }} from '../services/api';

export default function {pascal}List() {{
  const [items, setItems] = useState<any[]>([]);

  const fetchItems = async () => {{
    const res = await api.get('/{entity}');
    setItems(res.data);
  }};

  useEffect(() => {{
    fetchItems();
  }}, []);

  const handleDelete = async (id: string) => {{
    await api.delete(`/{entity}/${{id}}`);
    fetchItems();
  }};

  return (
    <div>
      <h1>{pascal} List</h1>
      <Link to="/{entity}/new">
        <button>Add New {pascal}</button>
      </Link>
      <table border={{1}} style={{{{ marginTop: "1rem" }}}}>
        <thead>
          <tr>
            <th>ID</th>
            {f"<th>{display_col.title()}</th>" if display_col != "id" else ""}
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {{items.map(item => (
            <tr key={{item.id}}>
              <td>{{item.id}}</td>
              {f"<td>{{item.{display_col}}}</td>" if display_col != "id" else ""}
              <td>
                <Link to={{`/{entity}/edit/${{item.id}}`}}>
                  <button>Edit</button>
                </Link>
                <button onClick={{() => handleDelete(item.id)}} style={{{{ marginLeft: "0.5rem" }}}}>Delete</button>
              </td>
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  );
}}
"""

    def _gen_entity_form(self, entity: str, pascal: str, props: dict) -> str:
        # Construct form fields dynamically from openapi properties
        form_fields = []
        state_init = []
        for p_name in props.keys():
            if p_name == "id": continue
            form_fields.append(f"""
        <div>
          <label>{p_name.title()}: </label>
          <input 
            value={{formData.{p_name} || ''}} 
            onChange={{e => setFormData({{
            ...formData,
            {p_name}: e.target.value
          }})}} 
          />
        </div>
            """)
            state_init.append(f"{p_name}: ''")
            
        initial_state = "{ " + ", ".join(state_init) + " }"
        
        return f"""import React, {{ useEffect, useState }} from 'react';
import {{ useNavigate, useParams }} from 'react-router-dom';
import {{ api }} from '../services/api';

export default function {pascal}Form() {{
  const [formData, setFormData] = useState<any>({initial_state});
  const navigate = useNavigate();
  const {{ id }} = useParams();
  const isEdit = Boolean(id);

  useEffect(() => {{
    if (isEdit) {{
      api.get(`/{entity}/${{id}}`).then(res => setFormData(res.data));
    }}
  }}, [id, isEdit]);

  const handleSubmit = async (e: React.FormEvent) => {{
    e.preventDefault();
    if (isEdit) {{
      await api.put(`/{entity}/${{id}}`, formData);
    }} else {{
      await api.post('/{entity}', formData);
    }}
    navigate('/{entity}');
  }};

  return (
    <div>
      <h1>{{isEdit ? 'Edit' : 'Create'}} {pascal}</h1>
      <form onSubmit={{handleSubmit}}>
        {"".join(form_fields)}
        <br />
        <button type="submit">Save</button>
        <button type="button" onClick={{() => navigate('/{entity}')}} style={{{{ marginLeft: "0.5rem" }}}}>Cancel</button>
      </form>
    </div>
  );
}}
"""

    def _gen_app_tsx(self, entities: List[str]) -> str:
        imports = []
        routes = []
        links = []
        
        for entity in entities:
            pascal = self._to_pascal_case(entity)
            imports.append(f"import {pascal}List from './pages/{pascal}List';")
            imports.append(f"import {pascal}Form from './pages/{pascal}Form';")
            
            links.append(f'        <Link to="/{entity}" style={{{{marginRight: "1rem"}}}}>{entity.replace("_", " ").title()}</Link>')
            
            routes.append(f'          <Route path="/{entity}" element={{<{pascal}List />}} />')
            routes.append(f'          <Route path="/{entity}/new" element={{<{pascal}Form />}} />')
            routes.append(f'          <Route path="/{entity}/edit/:id" element={{<{pascal}Form />}} />')

        imports_str = "\n".join(imports)
        links_str = "\n".join(links)
        routes_str = "\n".join(routes)
        
        return f"""import React from 'react';
import {{ BrowserRouter, Routes, Route, Link }} from 'react-router-dom';
{imports_str}

function Home() {{
  return (
    <div>
      <h1>Aayu Generated Dashboard</h1>
      <p>Welcome to your full-stack application.</p>
    </div>
  );
}}

export default function App() {{
  return (
    <BrowserRouter>
      <nav style={{{{ padding: '1rem', background: '#f0f0f0', marginBottom: '2rem' }}}}>
        <Link to="/" style={{{{marginRight: "2rem", fontWeight: "bold"}}}}>Home</Link>
{links_str}
      </nav>
      <div style={{{{ padding: '0 2rem' }}}}>
        <Routes>
          <Route path="/" element={{<Home />}} />
{routes_str}
        </Routes>
      </div>
    </BrowserRouter>
  );
}}
"""
