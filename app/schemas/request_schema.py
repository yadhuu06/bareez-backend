from pydantic import BaseModel
from typing import Optional
from .room_schema import Room
from .guest_schema import Guest

class RequestBase(BaseModel):
    description: str
    status: Optional[str] = "Pending"

class RequestCreate(RequestBase):
    room_id: int
    guest_id: int


class RequestUpdate(BaseModel):
    status: str


class Request(RequestBase):
    id: int
    room_id: int
    guest_id: int
    room: Room
    guest: Guest

    class Config:
        from_attributes = True