# Bandle - Modular Application

This is a modular application architecture featuring a Next.js frontend and a FastAPI backend.

## Structure

- `/frontend`: Next.js 15+ (App Router), Framer Motion, Tailwind CSS 4.
- `/backend`: FastAPI Python backend.

## Getting Started

### Backend Setup

1. Navigate to the `backend` directory.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the `frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Development

The frontend is configured to communicate with the backend at `http://localhost:8000`. Make sure the backend is running to see live data on the home page.
