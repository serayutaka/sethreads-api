from pydantic import BaseModel
from typing import List

class CourseBase(BaseModel):
    id: str

class CourseCreate(BaseModel):
    id: str
    name: str
    require_year: int

class Course(CourseBase):
    name: str
    require_year: int

    class Config:
        orm_mode = True