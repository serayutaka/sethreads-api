from pydantic import BaseModel
from typing import List


class StudentBase(BaseModel):
    student_id: str

class StudentCreate(StudentBase):
    password: str

class StudentWithCourses(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    picture: bytes | None
    ta_course_id: str | None

    registered_courses: List['Course'] = [] #type: ignore

    class Config:
        orm_mode = True

class StudentWithThreads(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    picture: bytes | None
    ta_course_id: str | None

    posted: List['Thread'] = [] #type: ignore

    class Config:
        orm_mode = True

class Student(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    picture: bytes | None
    ta_course_id: str | None

    class Config:
        orm_mode = True

