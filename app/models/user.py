from sqlalchemy import Column, Integer, String,  Enum
from app.db.base_class import Base
from app.schemas.user_schema import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STAFF, nullable=False)