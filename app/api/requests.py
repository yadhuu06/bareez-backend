import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.schemas.request_schema import Request, RequestCreate, RequestUpdate
from app.crud import request_crud, room_crud, guest_crud
from app.db.session import get_db
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_manager
from app.core.websocket_manager import manager 
router = APIRouter()


@router.post("/requests", response_model=Request, status_code=status.HTTP_201_CREATED, tags=["requests"])
async def create_new_request(
    request: RequestCreate,
    db: Session = Depends(get_db)
):
    """
    Webhook to receive a new service request from another system.
    It validates that the room and guest exist before creating the request.
    It broadcasts the new request to all connected clients.
    """
    db_room = room_crud.get_room(db, room_id=request.room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_guest = guest_crud.get_guest(db, guest_id=request.guest_id)
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")
        
    db_request = request_crud.create_request(db=db, request=request)

    try:
        request_pydantic = Request.from_orm(db_request)

        payload_data = request_pydantic.model_dump() 


        await manager.broadcast(
            {
                "type": "NEW_REQUEST",
                "payload": payload_data
            }
        )
    except Exception as e:
        print(f"Error broadcasting NEW_REQUEST: {e}")
        
    return db_request


@router.get("/requests", response_model=List[Request], tags=["requests"])
def read_requests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    """
    Fetches a list of all service requests (paginated).
    Requires a valid JWT from any authenticated user.
    """
    requests = request_crud.get_requests(db, skip=skip, limit=limit)
    return requests


@router.patch("/requests/{request_id}", response_model=Request, tags=["requests"])
async def update_request_status(
    request_id: int,
    request_update: RequestUpdate,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager) 
):
    """
    Updates a request's status (Manager role-protected).
    It broadcasts the updated request to all connected clients.
    """
    db_request = request_crud.get_request(db, request_id=request_id)
    if not db_request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    updated_request = request_crud.update_request(db=db, db_request=db_request, request_update=request_update)
    

    try:
        updated_request_pydantic = Request.from_orm(updated_request)

        payload_data = updated_request_pydantic.model_dump()
   

        await manager.broadcast(
            {
                "type": "REQUEST_UPDATE",
                "payload": payload_data
            }
        )
    except Exception as e:
        print(f"Error broadcasting REQUEST_UPDATE: {e}")
        
    return updated_request