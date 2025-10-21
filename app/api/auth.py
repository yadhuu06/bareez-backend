from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, User, Token
from app.crud.user import get_user_by_email, create_user
from app.core.security import create_access_token, verify_password
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handles user registration.
    Checks if the email already exists and then creates the new user.
    """
    db_user = get_user_by_email(db, email=user.email) 
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return create_user(db=db, user=user) 


@router.post("/login", response_model=Token) 
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Handles user login and returns a JWT access token AND user role.
    """

    user = get_user_by_email(db, email=form_data.username) 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.email})
    

    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user_role": user.role.value 
    }
