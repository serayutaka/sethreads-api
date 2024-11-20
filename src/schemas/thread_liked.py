from pydantic import BaseModel

class ThreadLikedBase(BaseModel):
    course_id: str
    thread_id: int
    student_id: str