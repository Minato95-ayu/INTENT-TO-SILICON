import os

class RuntimeGenerator:
    def generate_backend_runtime(self, entities):
        """Generates main.py and requirements.txt for FastAPI"""
        
        main_code = """import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aayu Generated API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Aayu Generated Production Runtime"}

# --- Routers ---
"""
        for entity in entities:
            main_code += f"from routers import {entity}_api\n"
            main_code += f"app.include_router({entity}_api.router, tags=['{entity}'])\n"

        main_code += """
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""
        
        requirements = """fastapi==0.103.1
uvicorn==0.23.2
sqlalchemy==2.0.20
pydantic==2.3.0
"""
        return main_code, requirements

    def generate_frontend_runtime(self, modules):
        """Generates package.json, vite.config.ts, and React root files"""
        
        package_json = """{
  "name": "aayu-generated-app",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.5.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.15",
    "@types/react-dom": "^18.2.7",
    "@vitejs/plugin-react": "^4.0.3",
    "typescript": "^5.0.2",
    "vite": "^4.4.5"
  }
}
"""
        
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
})
"""

        tsconfig = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,

    /* Bundler mode */
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",

    /* Linting */
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""

        main_tsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

        imports = []
        components = []
        for mod in modules:
            name_camel = ''.join(x.title() for x in mod.split('_'))
            imports.append(f"import {name_camel} from './components/{name_camel}'")
            components.append(f"        <{name_camel} />")
            
        imports_str = "\n".join(imports)
        components_str = "\n".join(components)

        app_tsx = f"""import React from 'react'
{imports_str}

function App() {{
  return (
    <div>
      <h1>Aayu Generated App</h1>
      <div className="components-grid">
{components_str}
      </div>
    </div>
  )
}}

export default App
"""

        index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Aayu Generated App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

        return package_json, vite_config, tsconfig, main_tsx, app_tsx, index_html
