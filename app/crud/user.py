from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Fetches a user from the database by their email address.
    """
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Creates a new user in the database.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
        # The role defaults to 'Staff' as defined in the model
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
