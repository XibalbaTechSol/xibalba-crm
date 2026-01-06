# Gemini CLI Context & Operational Guidelines

## 1. Project Overview
**Name:** Xibalba CRM
**Goal:** A modern healthcare CRM platform migrated from EspoCRM.
**Architecture:** Headless architecture with a Python API backend and a React Single Page Application (SPA) frontend.

## 2. Technology Stack

### Backend (`python/`)
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** MySQL/MariaDB (using SQLAlchemy for ORM)
- **Authentication:** JWT (JSON Web Tokens)
- **Conventions:** PEP 8, Type hints (Pydantic models).

### Frontend (`client-react/`)
- **Library:** React (Functional components, Hooks)
- **Build Tool:** Vite
- **Language:** JavaScript/TypeScript (Prefer TypeScript where possible)
- **Styling:** CSS Modules or Tailwind (verify in project).

## 3. Directory Structure
- `/python`: The backend API server.
- `/client-react`: The frontend React application.
- `legacy_*.tar.gz`: Archives of the old PHP/JS codebase (reference only).

## 4. Operational Guidelines
- **Tools First:** Always check file content before editing. Do not guess framework specifics.
- **Safety:** Do not delete `legacy_*.tar.gz` archives without explicit permission.
- **Git:** Commit often with clear messages. Push to `main` only when stable.
- **Secrets:** NEVER commit `.env` files or secrets to git.

## 5. Common Tasks
- **Start Backend:**
  ```bash
  cd python
  source venv/bin/activate
  python -m uvicorn app.main:app --reload
  ```
- **Start Frontend:**
  ```bash
  cd client-react
  npm run dev
  ```
