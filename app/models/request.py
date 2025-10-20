from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base



class Request(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String, default="Pending")
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))
