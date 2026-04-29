from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Bandle Booking"
    SECRET_KEY: str = "this-is-a-super-secret-development-key-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 # 24 hours
    
    # Database URLs
    PG_DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/booking_app"
    MONGO_DATABASE_URL: str = "mongodb://mongo:27017"
    
    # Security Configuration
    CSRF_SECRET: str = "csrf-super-secret-key-change-me"
    COOKIE_DOMAIN: str | None = None # Set to your domain in prod
    SECURE_COOKIES: bool = False # Set to True in prod (HTTPS)

    class Config:
        env_file = ".env"

settings = Settings()
