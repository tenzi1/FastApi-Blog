from sqlalchemy.orm import Session
from db.models.blog import Blog
from schemas.blog import CreateBlog


def create_new_blog(blog: CreateBlog, db: Session, author_id: int):
    blog = Blog(**blog.model_dump(), author_id=author_id)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog


def list_blogs(skip: int, limit: int, db: Session):
    blogs = (
        db.query(Blog).filter(Blog.is_active == True).offset(skip).limit(limit).all()
    )
    return blogs
