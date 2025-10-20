from pydantic import BaseModel
from typing import Optional

class GuestBase(BaseModel):
    name: str
    room_id: int

class GuestCreate(GuestBase):
    pass

class Guest(GuestBase):
    id: int

    class Config:
        from_attributes = True

