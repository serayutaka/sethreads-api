from pydantic import BaseModel

from .threads import Thread

class CourseBase(BaseModel):
    course_id: str
    name: str

class CourseCreate(CourseBase):
    pass

class Course(CourseBase):
    student_id: int

    forums: list[Thread] = []
    class Config:
        orm_mode = True