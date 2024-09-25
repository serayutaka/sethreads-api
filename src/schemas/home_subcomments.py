from pydantic import BaseModel
from typing import List, Optional


class HomeSubCommentBase(BaseModel):
    reply_of: int

class HomeSubCommentCreate(HomeSubCommentBase):
    reply_data: str
    posted_by: str
    create_at: str

class HomeSubCommentUpdate(BaseModel):
    reply_data: str
    create_at: str

class HomeSubCommentForStudent(HomeSubCommentBase):
    reply_data: str
    create_at: str

class HomeSubComment(HomeSubCommentBase):
    id: int
    reply_data: str
    create_at: str

    author: Optional['Student'] = None # type: ignore

    class Config:
        from_attributes = True
