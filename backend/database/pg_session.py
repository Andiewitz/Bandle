from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

# Replace with your actual PostgreSQL connection string
PG_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/booking_app"

engine = create_async_engine(PG_DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_pg_db():
    async with AsyncSessionLocal() as session:
        yield session
