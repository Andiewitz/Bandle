import motor.motor_asyncio
from pydantic import BaseModel

# Replace with your actual MongoDB connection string
MONGO_DATABASE_URL = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DATABASE_URL)
mongo_db = client.booking_app

def get_mongo_db():
    return mongo_db
