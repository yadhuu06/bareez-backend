from sqlalchemy import Column, Integer, String
from app.db.base import Base


class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True)
