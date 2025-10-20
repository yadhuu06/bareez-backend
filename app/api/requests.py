from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.request_schema import Request, RequestCreate, RequestUpdate
from app.crud import request_crud, room_crud, guest_crud
from app.db.session import get_db
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_manager

router = APIRouter()


@router.post("/requests", response_model=Request, status_code=status.HTTP_201_CREATED, tags=["requests"])
def create_new_request(
    request: RequestCreate,
    db: Session = Depends(get_db)
):
    """
    Webhook to receive a new service request from another system.
    It validates that the room and guest exist before creating the request.
    """
    db_room = room_crud.get_room(db, room_id=request.room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_guest = guest_crud.get_guest(db, guest_id=request.guest_id)
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
        
    return request_crud.create_request(db=db, request=request)


@router.get("/requests", response_model=List[Request], tags=["requests"])
def read_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    Fetches a list of all service requests.
    Requires a valid JWT from any authenticated user (Staff or Manager).
    """
    requests = request_crud.get_requests(db, skip=skip, limit=limit)
    return requests


@router.patch("/requests/{request_id}", response_model=Request, tags=["requests"])
def update_request_status(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager) 
):

    db_request = request_crud.get_request(db, request_id=request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    return request_crud.update_request(db=db, db_request=db_request, request_update=request_update)
