from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from app.db.session import get_db
from app.crud import room_crud, guest_crud
from app.schemas.room_schema import RoomCreate, Room
from app.schemas.guest_schema import GuestCreate, Guest

router = APIRouter(prefix="/setup", tags=["setup"])

# --- Initial Seed Data ---

INITIAL_ROOMS = [
    {"number": "101"},
    {"number": "205"},
    {"number": "312"},
]

INITIAL_GUESTS = [
    {"name": "Alice Johnson", "room_number": "101"},
    {"name": "Bob Smith", "room_number": "205"},
    {"name": "Charlie Brown", "room_number": "101"}, 
]

# --------------------------


@router.post("/seed-initial-data", response_model=Dict[str, int], status_code=status.HTTP_201_CREATED)
def seed_initial_data(db: Session = Depends(get_db)):

    
    
    created_rooms_count = 0
    room_number_to_id: Dict[str, int] = {}
    
    for room_data in INITIAL_ROOMS:
        room_number = room_data["number"]
        
        existing_room = room_crud.get_room_by_number(db, number=room_number)
        
        if not existing_room:
            room_create = RoomCreate(number=room_number)
            db_room = room_crud.create_room(db, room=room_create)
            room_number_to_id[room_number] = db_room.id
            created_rooms_count += 1
        else:
            room_number_to_id[room_number] = existing_room.id
            
    # --- 2. Create Guests ---
    created_guests_count = 0
    for guest_data in INITIAL_GUESTS:
        room_number = guest_data["room_number"]
        guest_name = guest_data["name"]
        
        if room_number not in room_number_to_id:

            continue 

        room_id = room_number_to_id[room_number]
        

        guest_create = GuestCreate(name=guest_name, room_id=room_id)
        guest_crud.create_guest(db, guest=guest_create)
        created_guests_count += 1

    return {
        "rooms_created": created_rooms_count,
        "guests_created": created_guests_count
    }