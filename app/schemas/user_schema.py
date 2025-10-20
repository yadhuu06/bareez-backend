# app/schemas/user_schema.py
import enum
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserRole(str, enum.Enum):
    STAFF = "Staff"
    MANAGER = "Manager"

class UserCreate(BaseModel):
    email: EmailStr  
    password: str
    username: Optional[str] = None
    


class User(BaseModel):
    id: int
    email: EmailStr
    username: Optional[str] = None
    role: UserRole

    class Config:
        from_attributes = True