# Xibalba CRM Implementation Plan

This document tracks the migration and development status of Xibalba CRM, moving from the legacy EspoCRM (PHP) codebase to a modern Python (FastAPI) and React architecture.

## Phase 1: Cleanup & Migration Preparation
- [x] **Archive Legacy Code:** Original PHP application archived to `legacy_php_code.tar.gz`.
- [x] **Remove Legacy Assets:** Old build tools (Grunt), frontend source (client/frontend), and node_modules removed.
- [x] **Repository Cleanup:** Deleted extraneous config files (`package.json`, `composer.json`) from root.

## Phase 2: Python Backend (FastAPI)
**Directory:** `python/`

- [x] **Initial Setup:** FastAPI app structure and basic configuration.
- [x] **Core Services:**
    - [x] Metadata Service (merging JSON configs).
    - [x] Language/I18n Service.
    - [x] Basic Client Bootstrapping.
- [ ] **Authentication & Security:**
    - [ ] Implement JWT token generation and validation.
    - [ ] Password hashing (Argon2 or bcrypt).
    - [ ] Login/Logout API endpoints.
- [ ] **Data Access Layer (ORM):**
    - [ ] Configure SQLAlchemy with the existing database schema.
    - [ ] Create generic CRUD Service.
    - [ ] Implement dynamic entity mapping based on Espo metadata.
- [ ] **API Development:**
    - [ ] CRUD endpoints for standard entities (Account, Contact, etc.).
    - [ ] Search and filtering logic (`SelectManager` equivalent).
    - [ ] Relationship handling (link/unlink).

## Phase 3: React Frontend
**Directory:** `client-react/`

- [x] **Scaffolding:** Vite project initialized with React.
- [ ] **Core Architecture:**
    - [ ] API Client setup (Axios/Fetch with interceptors).
    - [ ] Auth Context/Provider (Login state management).
    - [ ] Routing (React Router).
- [ ] **UI Components:**
    - [ ] Layout (Navbar, Sidebar, Main Content area).
    - [ ] Generic "Record" views (List, Detail, Edit).
    - [ ] Dynamic form generation based on Metadata.
- [ ] **Feature Parity:**
    - [ ] Replicate core CRM views (Accounts, Contacts).
    - [ ] Implement Search/Filter UI.

## Phase 4: Integration & Testing
- [ ] **End-to-End Testing:** Verify flow from React Login -> FastAPI Auth -> Database.
- [ ] **Deployment:** Create Dockerfile and docker-compose for the full stack.
