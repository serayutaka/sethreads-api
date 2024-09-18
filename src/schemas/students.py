from pydantic import BaseModel
from typing import List


class StudentBase(BaseModel):
    student_id: str

class StudentCreate(StudentBase):
    password: str

class Student(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    picture: bytes | None
    ta_course_id: str | None

    class Config:
        orm_mode = True

class StudentAllAttributes(Student):
    registered_courses: List['Course'] = [] #type: ignore
    posted: List['ThreadForStudent'] = [] #type: ignore
    comment: List['CommentForStudent'] = [] #type: ignore
    reply: List['SubCommentForStudent'] = [] #type: ignore