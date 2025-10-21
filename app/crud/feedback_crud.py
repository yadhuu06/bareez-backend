from sqlalchemy.orm import Session, joinedload
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate
from typing import Optional, List, TypeVar, Type

ModelType = TypeVar("ModelType", bound=Type[Feedback])

def get_feedback(db: Session, feedback_id: int) -> Optional[Feedback]:
    return db.query(Feedback).options(
        joinedload(Feedback.room), 
        joinedload(Feedback.guest)
    ).filter(Feedback.id == feedback_id).first()

def get_all_feedback(db: Session, skip: int = 0, limit: int = 100) -> List[Feedback]:
    return db.query(Feedback).options(
        joinedload(Feedback.room), 
        joinedload(Feedback.guest)
    ).offset(skip).limit(limit).all()

def create_feedback(db: Session, feedback: FeedbackCreate, sentiment: str) -> Feedback:

    db_feedback = Feedback(**feedback.dict(), sentiment=sentiment)
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)

    return get_feedback(db, db_feedback.id)