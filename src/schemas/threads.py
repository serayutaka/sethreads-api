from pydantic import BaseModel

from .students import Student
from .thread_pictures import ThreadPictures

class ThreadBase(BaseModel):
    id: int
    course_id: int

class ThreadCreate(ThreadBase):
    title: str
    body: str
    is_highlight: bool | False
    create_at: str

    pictures: list[ThreadPictures] = []

class Thread(ThreadBase):
    title: str
    body: str
    is_highlight: bool | False
    create_at: str

    pictures: list[ThreadPictures] = []
    author: Student




