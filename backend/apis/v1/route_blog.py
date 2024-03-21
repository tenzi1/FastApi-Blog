from typing import List

from db.repository.blog import create_new_blog
from db.repository.blog import delete_blog
from db.repository.blog import list_blogs
from db.repository.blog import retrieve_blog
from db.repository.blog import update_blog
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from schemas.blog import CreateBlog
from schemas.blog import ShowBlog
from schemas.blog import UpdateBlog
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/blogs", response_model=ShowBlog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    blog = create_new_blog(db=db, blog=blog, author_id=1)
    return blog


@router.get("/blog/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id=id, db=db)
    if not blog:
        raise HTTPException(
            detail=f"Blog with ID {id} does not exists.",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return blog


@router.get("/blogs", response_model=List[ShowBlog])
def get_all_blogs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    blogs = list_blogs(skip=skip, limit=limit, db=db)
    return blogs


@router.put("/blog/{id}", response_model=ShowBlog)
def update_a_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db)):
    blog = update_blog(id=id, blog=blog, db=db)
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} doesn't exist.",
        )
    return blog


@router.delete("/delete/{id}")
def delete_a_blog(id: int, db: Session = Depends(get_db)):
    message = delete_blog(id=id, db=db)
    if message.get("error"):
        raise HTTPException(
            detail=message.get("error"), status_code=status.HTTP_404_NOT_FOUND
        )
    return message
