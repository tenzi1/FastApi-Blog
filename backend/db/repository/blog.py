from db.models.blog import Blog
from schemas.blog import CreateBlog
from schemas.blog import UpdateBlog
from sqlalchemy.orm import Session


def create_new_blog(blog: CreateBlog, db: Session, author_id: int):
    blog = Blog(**blog.model_dump(), author_id=author_id, is_active=True)
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


def update_blog(id: int, blog: UpdateBlog, author_id: int, db: Session):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error": f"blog with id {id} does not exist."}
    if not blog_in_db.author_id == author_id:
        return {"error": "Only the author can modify the blog."}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db


def delete_blog(id: int, author_id: int, db: Session):
    try:
        blog_in_db = db.query(Blog).filter(Blog.id == id).first()
        if not blog_in_db:
            return {"error": f"Could not find blog with id {id}"}
        if not blog_in_db.author_id == author_id:
            return {"error": "Only the author can delete a blog"}
        db.delete(blog_in_db)
        db.commit()
        return {"message": f"Successfully deleted blog with id {id}"}
    except Exception as e:
        return {"error": f"{e}"}
