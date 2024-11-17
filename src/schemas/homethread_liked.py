from pydantic import BaseModel

class HomeThreadLikedBase(BaseModel):
    thread_id: int
    student_id: str