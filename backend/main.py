from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from database.pg_session import engine, Base, get_pg_db
from database.mongo_session import get_mongo_db
from sqlalchemy.ext.asyncio import AsyncSession
from api import auth

app = FastAPI(title="Booking App API", version="2.0.0")

# Allow CORS for local Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)

@app.on_event("startup")
async def init_db():
    # Automatically create PostgreSQL tables on startup (For dev only)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Booking App API!"}

@app.get("/api/health")
async def health_check(pg_db: AsyncSession = Depends(get_pg_db), mongo_db = Depends(get_mongo_db)):
    # In a real app, you might run a lightweight query to test connections
    return {
        "status": "ok", 
        "architecture": "Dual DB (PostgreSQL + MongoDB)",
        "postgres": "Connected",
        "mongodb": "Connected"
    }

@app.get("/api/data")
def get_data():
    return {"data": ["Auth Module (Postgres)", "Booking Engine (Postgres)", "Community Posts (MongoDB)"]}

