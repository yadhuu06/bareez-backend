from pydantic import BaseModel
from typing import Optional
from .room_schema import Room
from .guest_schema import Guest

class FeedbackBase(BaseModel):
    message: str
    room_id: int
    guest_id: int


class FeedbackCreate(FeedbackBase):
    pass


class Feedback(FeedbackBase):
    id: int
    sentiment: Optional[str]
    room: Room
    guest: Guest

    class Config:
        from_attributes = True