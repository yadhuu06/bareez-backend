from sqlalchemy.orm import Session
from app.models.room import Room
from app.schemas.room_schema import RoomCreate
from typing import Optional, List

def get_room(db: Session, room_id: int) -> Optional[Room]:

    return db.query(Room).filter(Room.id == room_id).first()


def get_room_by_number(db: Session, number: str) -> Optional[Room]:
    
    return db.query(Room).filter(Room.number == number).first()

def create_room(db: Session, room: RoomCreate) -> Room:
    db_room = Room(number=room.number)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def get_all_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[Room]:
    return db.query(Room).offset(skip).limit(limit).all()
