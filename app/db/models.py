from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.db.base import Base
from sqlalchemy.orm import relationship
from app.schemas.user_schema import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.STAFF, nullable=False)
    
class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True)

class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String, default="Pending")
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    sentiment = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))