from pydantic import BaseModel

from .courses import Course
from .threads import Thread
from .comments import Comment
from .subcomments import SubComment


class StudentBase(BaseModel):
    id: int

class StudentCreate(StudentBase):
    student_id: str
    password: str

class Student(StudentBase):
    student_id: str
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    picture: bytes | None
    ta_course_id: int | None

    registered_courses: list[Course] = []
    posted: list[Thread] = []
    comment: list[Comment] = []
    reply: list[SubComment] = []

    class Config:
        orm_mode = True

