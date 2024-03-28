from typing import Optional

from apis.v1.route_login import get_current_user
from db.repository.blog import create_new_blog
from db.repository.blog import delete_blog
from db.repository.blog import list_blogs
from db.repository.blog import retrieve_blog
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.templating import Jinja2Templates
from schemas.blog import CreateBlog
from sqlalchemy.orm import Session


templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
def home(
    request: Request,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    alert: Optional[str] = None,
):
    blogs = list_blogs(skip=skip, limit=limit, db=db)
    return templates.TemplateResponse(
        "blog/home.html", {"request": request, "blogs": blogs, "alert": alert}
    )


@router.get("/app/blog/{id}")
def blog_detail(
    request: Request,
    id: int,
    db: Session = Depends(get_db),
):
    blog = retrieve_blog(id=id, db=db)
    return templates.TemplateResponse(
        "blog/detail.html", {"request": request, "blog": blog}
    )


@router.get("/app/create-new-blog")
def get_blog_template(request: Request):
    return templates.TemplateResponse("blog/create_blog.html", {"request": request})


@router.post("/app/create-new-blog")
def create_blog(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db),
):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        blog = CreateBlog(title=title, content=content)
        blog = create_new_blog(blog=blog, db=db, author_id=author.id)
        return responses.RedirectResponse(
            "/?alert=Blog Submitted for Review", status_code=status.HTTP_302_FOUND
        )
    except Exception:
        errors = ["Please log in to create blog"]
        return templates.TemplateResponse(
            "blog/create_blog.html",
            {"request": request, "errors": errors, "title": title, "content": content},
        )


@router.get("/delete/{id}")
def delete_a_blog(request: Request, id: int, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    _, token = get_authorization_scheme_param(token)
    try:
        author = get_current_user(token=token, db=db)
        print("herererererer")
        msg = delete_blog(id=id, author_id=author.id, db=db)
        print("message", msg)
        alert = msg.get("error") or msg.get("message")
        print("alert")
        return responses.RedirectResponse(
            f"/?alert={alert}", status_code=status.HTTP_302_FOUND
        )
    except Exception:
        blog = retrieve_blog(id=id, db=db)
        return templates.TemplateResponse(
            "blog/detail.html",
            {"request": request, "alert": "Please login again", "blog": blog},
        )
