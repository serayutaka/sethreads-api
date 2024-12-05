from pydantic import BaseModel

class ThreadLikedBase(BaseModel):
    id: int

class ThreadLikedCreate(ThreadLikedBase):
    course_id: str
    thread_id: int
    student_id: str

class ThreadLiked(ThreadLikedBase):
    course_id: str
    thread_id: int
    student_id: str

    class Config:
        orm_mode = True