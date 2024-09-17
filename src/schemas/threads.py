from pydantic import BaseModel

from .thread_pictures import ThreadPictures

class ThreadBase(BaseModel):
    course_id: str

class ThreadCreate(ThreadBase):
    create_by: str
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str

class Thread(ThreadBase):
    create_by: str
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str




