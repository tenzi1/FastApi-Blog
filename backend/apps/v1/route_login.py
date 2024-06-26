import json

from core.hashing import Hasher
from core.security import create_access_token
from db.repository.login import get_user
from db.repository.user import create_new_user
from db.session import get_db
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import Request
from fastapi import responses
from fastapi import status
from fastapi.templating import Jinja2Templates
from pydantic.error_wrappers import ValidationError
from schemas.user import UserCreate
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="templates")
router = APIRouter()


def authenticate_user(email: str, password: str, db: Session):
    user = get_user(email=email, db=db)
    if not user:
        return False
    if not Hasher.verify_password(password, user.password):
        return False
    return user


@router.get("/register")
def get_registration_form(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
def register(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    errors = []
    try:
        user = UserCreate(email=email, password=password)
        user_exist = get_user(email=user.email, db=db)
        if not user_exist:
            create_new_user(user=user, db=db)
            return responses.RedirectResponse(
                "/?alert=Successfully%20Regigstered", status_code=status.HTTP_302_FOUND
            )
        else:
            errors.append({"email": "This email address is already registered."})
            return templates.TemplateResponse(
                "auth/register.html", {"request": request, "errors": errors}
            )

    except ValidationError as e:
        errors_list = json.loads(e.json())
        for item in errors_list:
            errors.append(item.get("loc")[0] + ": " + item.get("msg"))
        return templates.TemplateResponse(
            "auth/register.html", {"request": request, "errors": errors}
        )


@router.get("/login")
def get_login_form(request: Request):
    return templates.TemplateResponse(request, "auth/login.html")


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    errors = []
    user = authenticate_user(email=email, password=password, db=db)
    if not user:
        errors.append("Incorrect email or password")
        return templates.TemplateResponse(
            "auth/login.html", {"request": request, "errors": errors}
        )
    access_token = create_access_token(data={"sub": email})
    response = responses.RedirectResponse(
        "/?alert=Successfully Logged In", status_code=status.HTTP_302_FOUND
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return response
