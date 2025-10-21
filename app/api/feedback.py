from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict

from app.schemas.feedback_schema import Feedback, FeedbackCreate
from app.crud import feedback_crud, room_crud, guest_crud
from app.db.session import get_db
from app.models.user import User
from app.api.dependencies import get_current_user, get_current_manager
from app.core.ai_service import get_ai_analysis_service

router = APIRouter()


@router.post("/feedback", response_model=Feedback, status_code=status.HTTP_201_CREATED, tags=["feedback"])
def create_new_feedback(
    feedback: FeedbackCreate,
    db: Session = Depends(get_db)
):

    db_room = room_crud.get_room(db, room_id=feedback.room_id)
    if not db_room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    db_guest = guest_crud.get_guest(db, guest_id=feedback.guest_id)
    if not db_guest:
        raise HTTPException(status_code=404, detail="Guest not found")

    
    ai_service = get_ai_analysis_service()
    sentiment = ai_service(service_type="sentiment", text=feedback.message)
    
    # 3. Create the feedback in the database
    return feedback_crud.create_feedback(db=db, feedback=feedback, sentiment=sentiment)


@router.post("/feedback/{feedback_id}/generate-response", response_model=Dict[str, str], tags=["feedback"])
def generate_smart_response(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_manager: User = Depends(get_current_manager) # Manager only
):
    """
    Generates a smart, empathetic response for a piece of negative feedback.
    Requires a valid JWT from a user with the 'Manager' role.
    """
    db_feedback = feedback_crud.get_feedback(db, feedback_id=feedback_id)
    if not db_feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    # For this feature, we only generate responses for negative feedback
    if db_feedback.sentiment != "Negative":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Smart responses can only be generated for negative feedback."
        )

    # Call the AI service to generate the response
    ai_service = get_ai_analysis_service()
    smart_response = ai_service(service_type="response", text=db_feedback.message)
    
    return {"response": smart_response}
