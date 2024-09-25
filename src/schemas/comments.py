from pydantic import BaseModel
from typing import List, Optional


class CommentBase(BaseModel):
    comment_from: int

class CommentCreate(CommentBase):
    comment_from: int
    comment_data: str
    posted_by: str
    create_at: str

class CommentUpdate(BaseModel):
    comment_data: str
    create_at: str

class CommentForStudent(CommentBase):
    comment_data: str
    create_at: str

class CommentForThread(CommentBase):
    id: int

class Comment(CommentBase):
    id: int
    comment_data: str
    create_at: str

    subcomments: List['SubComment'] = None # type: ignore
    author: Optional['Student'] = None # type: ignore

    class Config:
        from_attributes = True

