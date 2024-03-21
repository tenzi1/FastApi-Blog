from datetime import datetime
from pydantic import BaseModel, root_validator
from typing import Optional


class CreateBlog(BaseModel):
    title: str
    slug: str
    content: Optional[str] = None

    @root_validator(pre=True)
    def generate_slug(cls, values):
        if "title" in values:
            values["slug"] = values.get("title").replace(" ", "-").lower()
        return values


class ShowBlog(BaseModel):
    title: str
    content: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class UpdateBlog(CreateBlog):
    pass
