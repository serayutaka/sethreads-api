from pydantic import BaseModel
from typing import List

class EnrollmentBase(BaseModel):
    id: int

class EnrollmentCreate(BaseModel):
    course_id: str
    student_id: str

class Enrollment(EnrollmentBase):
    course_id: str
    student_id: str

    class Config:
        orm_mode = True
    