from pydantic import BaseModel


class SubCommentBase(BaseModel):
    reply_of: int
    posted_by: int

class SubCommentCreate(SubCommentBase):
    reply_data: str
    create_at: str

class SubComment(SubCommentBase):
    reply_data: str
    create_at: str


    class Config:
        orm_mode = True