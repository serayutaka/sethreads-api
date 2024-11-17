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
    ta_course_id: str | None
    likedThreads: List['ThreadLikedBase'] = [] #type: ignore
    likedHomeThreads: List['HomeThreadLikedBase'] = [] #type: ignore
    
    class Config:
        from_attributes = True

class Students(Student):
    registered_courses: List['Course'] = [] #type: ignore

class StudentAllAttributes(Student):
    registered_courses: List['Course'] = [] #type: ignore
    
    posted: List['ThreadForStudent'] = [] #type: ignore
    comment: List['CommentForStudent'] = [] #type: ignore
    reply: List['SubCommentForStudent'] = [] #type: ignore

    