from pydantic import BaseModel
from typing import List


class CommentBase(BaseModel):
    comment_from: int

class CommentCreate(CommentBase):
    comment_from: int
    comment_data: str
    posted_by: int
    create_at: str

class Comment(CommentBase):
    comment_data: str
    create_at: str

    subcomments: List['SubComment'] = [] # type: ignore
    author: List['Student'] = [] # type: ignore

    class Config:
        orm_mode = True

