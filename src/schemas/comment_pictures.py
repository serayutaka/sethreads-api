from pydantic import BaseModel


class CommentPicturesBase(BaseModel):
    from_comment: int

class CommentPicturesCreate(CommentPicturesBase):
    data: bytes

class CommentPictures(CommentPicturesBase):
    from_comment: int
    data: bytes

    class Config:
        orm_mode = True