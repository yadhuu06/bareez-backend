from sqlalchemy.orm import Session, joinedload
from app.models.request import Request
from app.schemas.request_schema import RequestCreate, RequestUpdate
from typing import Optional, List, TypeVar, Type


ModelType = TypeVar("ModelType", bound=Type[Request])

def get_request(db: Session, request_id: int) -> Optional[Request]:
    return db.query(Request).options(
        joinedload(Request.room), 
        joinedload(Request.guest)
    ).filter(Request.id == request_id).first()

def get_requests(db: Session, skip: int = 0, limit: int = 100) -> List[Request]:
    return db.query(Request).options(
        joinedload(Request.room), 
        joinedload(Request.guest)
    ).offset(skip).limit(limit).all()

def create_request(db: Session, request: RequestCreate) -> Request:

    db_request = Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return get_request(db, db_request.id)

def update_request(db: Session, db_request: Request, request_update: RequestUpdate) -> Request:

    update_data = request_update.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_request, key, value)
        
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    
    return get_request(db, db_request.id)
