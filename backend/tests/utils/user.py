from db.repository.user import create_new_user
from schemas.user import UserCreate
from sqlalchemy.orm import Session


def create_random_user(db: Session):
    user = UserCreate(email="test@gmail.com", password="testpassword")
    user = create_new_user(user=user, db=db)
    return user
