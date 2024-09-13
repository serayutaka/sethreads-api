from pydantic import BaseModel

from .threads import Thread
from .courses import Course
from .comments import Comment
from .subcomments import SubComment

class StudentBase(BaseModel):
    id: int

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    year: int
    is_ta: bool
    picture: bytes
    ta_course_id: int

    registered_courses: list[Course] = []
    posted: list[Thread] = []
    comment: list[Comment] = []
    reply: list[SubComment] = []

    class Config:
        orm_mode = True


