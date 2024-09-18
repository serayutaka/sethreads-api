from pydantic import BaseModel

from typing import List, Optional

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

    author: Optional['Student'] = None # type: ignore


