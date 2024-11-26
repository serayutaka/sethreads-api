from pydantic import BaseModel
from typing import List, Optional


class CommentBase(BaseModel):
    id: int

class CommentCreate(CommentBase):
    thread_id: int
    course_id: str
    body: str
    commented_by: str
    create_at: str

class CommentUpdate(BaseModel):
    body: str
    create_at: str

class Comment(CommentBase):
    thread_id: int
    course_id: str
    body: str
    commented_by: str
    create_at: str

    replies: List['SubComment'] = [] #type: ignore
    author: Optional['Student'] = None #type: ignore