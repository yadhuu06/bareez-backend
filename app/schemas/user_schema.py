# app/schemas/user_schema.py
import enum
from pydantic import BaseModel, EmailStr


class UserRole(str, enum.Enum):
    STAFF = "Staff"
    MANAGER = "Manager"

class UserCreate(BaseModel):
    email: EmailStr  
    password: str
    username: str | None = None 
    


class User(BaseModel):
    id: int
    email: EmailStr
    username: str | None
    role: UserRole

    class Config:
        from_attributes = True