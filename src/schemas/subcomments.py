from pydantic import BaseModel
from typing import List, Optional


class SubCommentBase(BaseModel):
    reply_of: int

class SubCommentCreate(SubCommentBase):
    posted_by: str
    reply_data: str
    create_at: str

class SubCommentUpdate(BaseModel):
    reply_data: str
    create_at: str

class SubCommentForStudent(SubCommentBase):
    reply_data: str
    create_at: str

class SubComment(SubCommentBase):
    posted_by: str
    reply_data: str
    create_at: str

    author: Optional['Student'] = [] # type: ignore

    class Config:
        orm_mode = True