from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.pg_session import get_pg_db
from models.pg_models import User
from schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from core.security import get_password_hash, verify_password, create_access_token, generate_csrf_token
from core.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_pg_db)):
    # 1. Validate if user already exists
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash password and save
    hashed_pwd = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(response: Response, user_data: UserLogin, db: AsyncSession = Depends(get_pg_db)):
    # 1. Retrieve user
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()
    
    # 2. Verify credentials
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 3. Generate Auth JWT and CSRF Token
    access_token = create_access_token(data={"sub": str(user.id)})
    csrf_token = generate_csrf_token()
    
    # 4. Set HTTPOnly Cookie for the JWT to protect against XSS
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax", # Strict in prod cross-origin
        domain=settings.COOKIE_DOMAIN,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    
    # 5. Return CSRF token to frontend (Frontend stores in memory and sends in headers)
    return {"message": "Login successful", "csrf_token": csrf_token}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token", domain=settings.COOKIE_DOMAIN)
    return {"message": "Logged out successfully"}
