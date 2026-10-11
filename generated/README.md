# AAYU_App

> Auto-generated full-stack application by **AAYU v1**.

## Project Overview
This project was scaffolded via **Intent-to-Silicon** architecture. 
The entire codebase was deterministically generated from your `.aayu` schema files.

## Architecture

- **Frontend:** React + Vite (Port 3000)
- **Backend:** FastAPI (Port 8000)
- **Database:** PostgreSQL 15 (Port 5432)

## 1. Local Setup

### Frontend (React)
```bash
cd frontend
npm install
npm run dev
```

### Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Database (PostgreSQL)
Load `database/schema.sql` into your local Postgres instance or run via Docker.

## 2. Docker Setup (Recommended)

To spin up the entire stack seamlessly:
```bash
docker-compose up --build
```

Access the application at `http://localhost:3000`.
