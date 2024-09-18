from pydantic import BaseModel
from typing import List

class CourseBase(BaseModel):
    course_id: str
    name: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    student_id: int

    forums: List['Thread'] = [] # type: ignore
    
    class Config:
        orm_mode = True