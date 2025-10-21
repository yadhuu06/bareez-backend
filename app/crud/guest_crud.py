from sqlalchemy.orm import Session
from app.models.guest import Guest
from app.schemas.guest_schema import GuestCreate
from typing import Optional, List

def get_guest(db: Session, guest_id: int) -> Optional[Guest]:
    return db.query(Guest).filter(Guest.id == guest_id).first()

def get_guests_by_room(db: Session, room_id: int) -> List[Guest]:
    return db.query(Guest).filter(Guest.room_id == room_id).all()

def create_guest(db: Session, guest: GuestCreate) -> Guest:
    db_guest = Guest(name=guest.name, room_id=guest.room_id)
    db.add(db_guest)
    db.commit()
    db.refresh(db_guest)
    return db_guest

def get_all_guests(db: Session, skip: int = 0, limit: int = 100) -> List[Guest]:

    return db.query(Guest).offset(skip).limit(limit).all()
