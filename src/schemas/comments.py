from pydantic import BaseModel

from .comment_pictures import CommentPictures
from .subcomments import SubComment


class CommentBase(BaseModel):
    id: int
    thread_id: int

class CommentCreate(CommentBase):
    comment_from: int
    comment_data: str
    posted_by: int
    create_at: str

class Comment(CommentBase):
    comment_data: str
    create_at: str

    pictures: list[CommentPictures] = []
    subcomments: list[SubComment] = []

