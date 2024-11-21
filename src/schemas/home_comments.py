from pydantic import BaseModel
from typing import List, Optional


class HomeCommentBase(BaseModel):
    comment_from: int

class HomeCommentCreate(HomeCommentBase):
    comment_data: str
    posted_by: str
    create_at: str

class HomeCommentUpdate(BaseModel):
    comment_data: str
    create_at: str

class HomeCommentForStudent(HomeCommentBase):
    comment_data: str
    create_at: str
    subcomments: List['HomeSubCommentBase'] = None # type: ignore

class HomeCommentForThread(HomeCommentBase):
    id: int

class HomeComment(HomeCommentBase):
    id: int
    comment_data: str
    create_at: str

    subcomments: List['HomeSubComment'] = None # type: ignore
    author: Optional['Student'] = None # type: ignore

    class Config:
        from_attributes = True

