# Xibalba CRM

**A modern, headless healthcare CRM platform.**

Xibalba CRM is an evolution of the EspoCRM platform, transitioned to a modern technology stack to provide better performance, maintainability, and developer experience.

## 🏗 Architecture

The application uses a headless architecture, separating the backend API from the frontend user interface.

*   **Backend:** Python (FastAPI) - Located in `python/`
*   **Frontend:** React (Vite) - Located in `client-react/`
*   **Database:** MySQL/MariaDB

## 🚀 Getting Started

### Backend (Python)

1.  Navigate to the python directory:
    ```bash
    cd python
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    # venv\Scripts\activate   # Windows
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the server:
    ```bash
    python -m uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000`.

### Frontend (React)

1.  Navigate to the client directory:
    ```bash
    cd client-react
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the development server:
    ```bash
    npm run dev
    ```
    The app will open at `http://localhost:5173`.

## 📂 Project Structure

*   `python/`: FastAPI application source code.
*   `client-react/`: React application source code.
*   `legacy_php_code.tar.gz`: Archive of the original PHP backend logic (for reference).
*   `legacy_assets.tar.gz`: Archive of the original frontend assets (for reference).

## 📜 License

This project is based on EspoCRM and is licensed under the [GNU AGPLv3](LICENSE.txt).