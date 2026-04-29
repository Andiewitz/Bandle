from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.config import settings
from database.pg_session import get_pg_db
from models.pg_models import User

async def get_current_user(request: Request, db: AsyncSession = Depends(get_pg_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Format expected: "Bearer <token>"
        scheme, _, token_value = token.partition(" ")
        if not token_value:
            token_value = token # Fallback if just token is stored
            
        payload = jwt.decode(token_value, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
    return user

async def verify_csrf(request: Request):
    """
    Middleware dependency to enforce CSRF validation on mutating endpoints.
    Requires the frontend to send an 'X-CSRF-Token' header.
    """
    if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
        csrf_header = request.headers.get("X-CSRF-Token")
        if not csrf_header:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="CSRF token missing or invalid")
        # Note: For production, this token should be validated against a signed cookie or Redis session store.
    return True
