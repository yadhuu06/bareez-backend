from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from typing import Optional

from app.core.config import settings
from app.db.session import get_db
from app.crud.user import get_user_by_email
from app.models.user import User
from app.schemas.user_schema import UserRole

from app.db.session import SessionLocal


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login") 

def get_email_from_token(token: str) -> Optional[str]:
    """Helper to extract email (sub) from JWT payload."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: Optional[str] = payload.get("sub")
        return email
    except JWTError:
        return None

def get_user_by_token(token: str) -> Optional[User]:
    """
    Validates token and fetches user without HTTP dependency injection (used for WebSockets).
    """
    email = get_email_from_token(token)
    if email is None:
        return None
        
    
    db = SessionLocal()
    try:
        user = get_user_by_email(db, email=email)
        return user
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    """Dependency for securing standard HTTP endpoints (Staff or Manager access)."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    email = get_email_from_token(token)
    if email is None:
        raise credentials_exception
    
    user = get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

def get_current_manager(current_user: User = Depends(get_current_user)) -> User:
    """Dependency for securing Manager-only HTTP endpoints."""
    if current_user.role != UserRole.MANAGER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges",
        )
    return current_user
