from pydantic import BaseModel
from typing import List, Optional


class SubCommentBase(BaseModel):
    id: int
    
class SubCommentCreate(BaseModel):
    comment_id: int
    body: str
    replied_by: str
    create_at: str

class SubCommentUpdate(BaseModel):
    body: str
    create_at: str

class SubComment(SubCommentBase):
    comment_id: int
    body: str
    replied_by: str
    create_at: str

    author: Optional['Author'] = None #type: ignore