from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship 
from app.db.base_class import Base

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    message = Column(String)
    sentiment = Column(String)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    guest_id = Column(Integer, ForeignKey("guests.id"))
    room = relationship("Room", backref="feedback_room")
    guest = relationship("Guest", backref="feedback_guest")
