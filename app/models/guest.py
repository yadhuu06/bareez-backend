from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from app.db.base_class import Base


class Guest(Base):
    __tablename__ = "guests"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))
