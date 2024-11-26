from pydantic import BaseModel
from typing import List


class StudentBase(BaseModel):
    id: str

class StudentCreate(StudentBase):
    password: str

class Author(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    ta_course_id: str | None

class Student(StudentBase):
    name: str
    surname: str
    year: int | None
    is_ta: bool | None
    ta_course_id: str | None
    
    registered: List['Enrollment'] = [] # type: ignore
    posted: List['Thread'] = [] # type: ignore
    liked: List['ThreadLiked'] = [] # type: ignore
    comment: List['Comment'] = [] # type: ignore
    reply: List['SubComment'] = [] # type: ignore