# Bandle Backend (FastAPI)

A lightweight FastAPI service for the Bandle application.

## Requirements

- Python 3.8+

## Setup

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Documentation (Swagger) can be found at `http://localhost:8000/docs`.
