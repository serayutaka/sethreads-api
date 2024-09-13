from pydantic import BaseModel

class ThreadPicturesBase(BaseModel):
    from_thread: int

class ThreadPicturesCreate(ThreadPicturesBase):
    data: bytes
    order: int

class ThreadPictures(BaseModel):
    from_thread: int
    data: bytes
    order: int

    class Config:
        orm_mode = True