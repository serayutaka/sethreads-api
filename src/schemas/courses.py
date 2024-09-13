from pydantic import BaseModel

from .students import Student
from .threads import Thread

class CourseBase(BaseModel):
    id: int
    name: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    student_id: int
    registered_by: Student
    forums: list[Thread] = []

    class Config:
        orm_mode = True