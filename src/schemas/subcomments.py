from pydantic import BaseModel
from typing import List


class SubCommentBase(BaseModel):
    reply_of: int

class SubCommentCreate(SubCommentBase):
    reply_data: str
    create_at: str

class SubComment(SubCommentBase):
    posted_by: int
    reply_data: str
    create_at: str

    author: List['Student'] = [] # type: ignore

    class Config:
        orm_mode = True