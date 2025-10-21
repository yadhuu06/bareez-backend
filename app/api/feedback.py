from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.schemas.feedback_schema import Feedback, FeedbackCreate
from app.crud import feedback_crud, room_crud, guest_crud
from app.db.session import get_db
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_manager
from app.core.ai_service import get_ai_analysis_service
from app.core.websocket_manager import manager # Assuming the manager is correctly imported

router = APIRouter()


@router.get("/feedback", response_model=List[Feedback], tags=["feedback"])
def read_all_feedback(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
 
    current_user: User = Depends(get_current_user) 
):
    """
    Fetches a list of all guest feedback messages.
    Requires a valid JWT from any authenticated user (Staff or Manager).
    """

    feedback = feedback_crud.get_all_feedback(db, skip=skip, limit=limit)
    return feedback


@router.post("/feedback", response_model=Feedback, status_code=status.HTTP_201_CREATED, tags=["feedback"])
async def create_new_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):
    """
    Webhook to receive new guest feedback, determine sentiment, and broadcast in real-time.
    """
    db_room = room_crud.get_room(db, room_id=feedback.room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_guest = guest_crud.get_guest(db, guest_id=feedback.guest_id)
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    
    ai_service = get_ai_analysis_service()
    sentiment = await ai_service(service_type="sentiment", text=feedback.message)
    

    db_feedback = feedback_crud.create_feedback(db=db, feedback=feedback, sentiment=sentiment)

    try:
        feedback_pydantic = Feedback.from_orm(db_feedback)
        
        await manager.broadcast(
            {
                "type": "NEW_FEEDBACK",
                "payload": feedback_pydantic.model_dump() 
            }
        )
    except Exception as e:
        print(f"Error broadcasting NEW_FEEDBACK: {e}")
        
    return db_feedback


@router.post("/feedback/{feedback_id}/generate-response", response_model=Dict[str, str], tags=["feedback"])
async def generate_smart_response(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager) 
):
    """
    Generates a smart, empathetic response for a piece of negative feedback (Manager role-protected).
    """
    db_feedback = feedback_crud.get_feedback(db, feedback_id=feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    
    if db_feedback.sentiment != "Negative":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Smart responses can only be generated for negative feedback."
        )


    ai_service = get_ai_analysis_service()
    
    smart_response = await ai_service(service_type="response", text=db_feedback.message)
    
    return {"response": smart_response}