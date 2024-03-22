from typing import List

from db.repository.user import create_new_user
from db.repository.user import list_users
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from schemas.user import ShowUser
from schemas.user import UserCreate
from sqlalchemy.orm import Session


router = APIRouter()


@router.post("/users", response_model=ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user = create_new_user(user=user, db=db)
    return user


@router.get("/users", response_model=List[ShowUser])
def get_list_of_users(db: Session = Depends(get_db)):
    users = list_users(db=db)
    return users
