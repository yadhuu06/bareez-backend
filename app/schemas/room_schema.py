from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    number: str

class RoomCreate(RoomBase):
    pass


class Room(RoomBase):
    id: int

    class Config:
        from_attributes = True
