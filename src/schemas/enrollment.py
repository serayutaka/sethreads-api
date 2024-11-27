from pydantic import BaseModel
from typing import List, Optional

class EnrollmentBase(BaseModel):
    id: int

class EnrollmentCreate(BaseModel):
    course_id: str
    student_id: str

class Enrollment(EnrollmentBase):
    student_id: str

    course: Optional["Course"] = [] #type: ignore

    class Config:
        orm_mode = True
    