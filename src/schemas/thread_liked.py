from pydantic import BaseModel

class ThreadLikedBase(BaseModel):
    thread_id: int
    student_id: str