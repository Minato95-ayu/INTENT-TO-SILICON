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
        self.has_auth = "/auth/login" in openapi_spec.get("paths", {})
        
        # 1. Base Project Files
        files["package.json"] = self._gen_package_json()
        files["vite.config.ts"] = self._gen_vite_config()
        files["tsconfig.json"] = self._gen_tsconfig()
        files["index.html"] = self._gen_index_html()
        files["src/main.tsx"] = self._gen_main_tsx()
        files["src/services/api.ts"] = self._gen_api_service()
        
        # 2. Auth Pages
        if self.has_auth:
            files["src/pages/Login.tsx"] = self._gen_login_page()
            files["src/pages/Register.tsx"] = self._gen_register_page()
        
        # 3. Entity Pages
        entity_data = []
        for entity in entities:
            pascal = self._to_pascal_case(entity)
            entity_data.append({"name": entity, "pascal": pascal})
            props = self._get_schema_properties(openapi_spec, entity)
            files[f"src/pages/{pascal}List.tsx"] = self._gen_entity_list(entity, pascal, props)
            files[f"src/pages/{pascal}Form.tsx"] = self._gen_entity_form(entity, pascal, props)
            
        # 4. App Routing
        files["src/App.tsx"] = self._gen_app_tsx(entity_data)
        
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
    "noFallthroughCasesInSwitch": false,
    "types": ["vite/client"]
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

// Ensure this matches your FastAPI backend URL or environment variable
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
});

// Intercept requests to attach JWT token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Intercept responses to redirect to login on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    } else if (error.response && error.response.status >= 400) {
      const data = error.response.data;
      const reqId = data?.request_id || error.response.headers?.['x-request-id'] || 'unknown';
      const msg = data?.detail || data?.error || 'Request Failed';
      alert(`${msg}\nReference: ${reqId}`);
    } else {
      alert(`Network Error\nReference: unknown`);
    }
    return Promise.reject(error);
  }
);
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
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const size = 20;

  const fetchItems = async () => {{
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('size', size.toString());
    if (search) params.append('search', search);
    
    const res = await api.get(`/{entity}?${{params.toString()}}`);
    setItems(res.data.items || []);
  }};

  useEffect(() => {{
    fetchItems();
  }}, [page]); // Re-fetch when page changes
  
  const handleSearch = (e: React.FormEvent) => {{
    e.preventDefault();
    setPage(1); // Reset to first page on new search
    fetchItems();
  }};

  const handleDelete = async (id: string) => {{
    await api.delete(`/{entity}/${{id}}`);
    fetchItems();
  }};

  return (
    <div>
      <h1>{pascal} List</h1>
      <div style={{{{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}}}>
        <Link to="/{entity}/new">
          <button>Add New {pascal}</button>
        </Link>
        <form onSubmit={{handleSearch}}>
          <input 
            type="text" 
            placeholder="Search..." 
            value={{search}} 
            onChange={{e => setSearch(e.target.value)}} 
          />
          <button type="submit" style={{{{ marginLeft: '0.5rem' }}}}>Search</button>
        </form>
      </div>
      <table border={{1}} width="100%">
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
          {{items.length === 0 && (
            <tr>
              <td colSpan={{3}} style={{{{ textAlign: 'center' }}}}>No records found.</td>
            </tr>
          )}}
        </tbody>
      </table>
      
      <div style={{{{ marginTop: '1rem', display: 'flex', gap: '1rem', alignItems: 'center' }}}}>
        <button disabled={{page <= 1}} onClick={{() => setPage(p => p - 1)}}>Previous</button>
        <span>Page {{page}}</span>
        <button onClick={{() => setPage(p => p + 1)}}>Next</button>
      </div>
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

    def _gen_login_page(self) -> str:
        return """import React, { useState } from 'react';
import { api } from '../services/api';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    const res = await api.post('/auth/login', params);
    localStorage.setItem('token', res.data.access_token);
    window.location.href = '/';
  };

  return (
    <form onSubmit={handleLogin}>
      <h1>Login</h1>
      <input type="text" placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button type="submit">Login</button>
    </form>
  );
}
"""

    def _gen_register_page(self) -> str:
        return """import React, { useState } from 'react';
import { api } from '../services/api';
import { useNavigate } from 'react-router-dom';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    await api.post('/auth/register', { username, password });
    navigate('/login');
  };

  return (
    <form onSubmit={handleRegister}>
      <h1>Register</h1>
      <input type="text" placeholder="Username" onChange={e => setUsername(e.target.value)} />
      <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
      <button type="submit">Register</button>
    </form>
  );
}
"""

    def _gen_app_tsx(self, entities: List[Dict]) -> str:
        imports = []
        for e in entities:
            imports.append(f"import {e['pascal']}List from './pages/{e['pascal']}List';")
            imports.append(f"import {e['pascal']}Form from './pages/{e['pascal']}Form';")
            
        if self.has_auth:
            imports.append("import Login from './pages/Login';")
            imports.append("import Register from './pages/Register';")
            
        routes = ["<Route path='/' element={<h2>Welcome to Aayu Generated App</h2>} />"]
        if self.has_auth:
            routes.append("<Route path='/login' element={<Login />} />")
            routes.append("<Route path='/register' element={<Register />} />")
            
        for e in entities:
            routes.append(f"<Route path='/{e['name']}' element={{<{e['pascal']}List />}} />")
            routes.append(f"<Route path='/{e['name']}/new' element={{<{e['pascal']}Form />}} />")
            routes.append(f"<Route path='/{e['name']}/edit/:id' element={{<{e['pascal']}Form />}} />")
            
        imports_str = "\n".join(imports)
        routes_str = "\n          ".join(routes)
        
        nav_links = [f"<Link to='/{e['name']}'>{e['pascal']}</Link>" for e in entities]
        nav_links_str = " | ".join(nav_links)
        
        auth_nav = ""
        if self.has_auth:
            auth_nav = """
        <div style={{ float: 'right' }}>
          <Link to="/login">Login</Link> | <Link to="/register">Register</Link> | 
          <button onClick={() => { localStorage.removeItem('token'); window.location.href='/login'; }}>Logout</button>
        </div>"""
        
        return f"""import React from 'react';
import {{ BrowserRouter as Router, Routes, Route, Link }} from 'react-router-dom';
{imports_str}

export default function App() {{
  return (
    <Router>
      <nav style={{{{ padding: '1rem', borderBottom: '1px solid #ccc' }}}}>
        <strong>Aayu App</strong> | {nav_links_str} {auth_nav}
      </nav>
      <div style={{{{ padding: '1rem' }}}}>
        <Routes>
          {routes_str}
        </Routes>
      </div>
    </Router>
  );
}}
"""
