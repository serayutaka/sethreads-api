from pydantic import BaseModel

from .students import Student


class SubCommentBase(BaseModel):
    reply_of: int
    posted_by: int

class SubCommentCreate(SubCommentBase):
    reply_data: str
    create_at: str

class SubComment(SubCommentBase):
    reply_data: str
    create_at: str

    author: Student

    class Config:
        orm_mode = True