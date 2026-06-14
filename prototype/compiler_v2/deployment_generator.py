"""
Aayu Deployment Generator

Generates containerization files (Dockerfile, docker-compose) for a full stack deployment.
"""
from typing import Dict

class DeploymentGenerator:
    def generate(self) -> Dict[str, str]:
        files = {}
        
        # 1. Backend Dockerfile
        files["backend/Dockerfile"] = self._gen_backend_dockerfile()
        
        # 2. Frontend Dockerfile
        files["frontend/Dockerfile"] = self._gen_frontend_dockerfile()
        
        # 3. docker-compose.yml
        files["docker-compose.yml"] = self._gen_docker_compose()
        
        # 4. .env.example
        files[".env.example"] = self._gen_env_example()
        
        # 5. Nginx config (optional but needed for React Router client-side routing)
        files["frontend/nginx.conf"] = self._gen_nginx_conf()
        
        return files

    def _gen_backend_dockerfile(self) -> str:
        return """FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

    def _gen_frontend_dockerfile(self) -> str:
        return """# Stage 1: Build
FROM node:20 AS build
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Serve
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
"""

    def _gen_nginx_conf(self) -> str:
        return """server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        try_files $uri $uri/ /index.html;
    }
}
"""

    def _gen_docker_compose(self) -> str:
        return """version: '3.8'

services:
  backend:
    build:
      context: ./backend
    ports:
      - "8000:8000"
    env_file:
      - .env
    volumes:
      - backend_data:/app

  frontend:
    build:
      context: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  backend_data:
"""

    def _gen_env_example(self) -> str:
        return """DATABASE_URL=sqlite:///./app.db
VITE_API_URL=http://localhost:8000
"""
