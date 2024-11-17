from pydantic import BaseModel
from typing import List

class CourseBase(BaseModel):
    course_id: str
    name: str

class CourseCreate(BaseModel):
    course_id: str
    student_id: str
    year: int

class Course(CourseBase):
    student_id: str
    year: int

    forums: List['Thread'] = [] # type: ignore
    
    class Config:
        from_attributes = True