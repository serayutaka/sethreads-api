from pydantic import BaseModel
from typing import List, Optional

class ThreadBase(BaseModel):
    id: int

class ThreadCreate(BaseModel):
    course_id: str
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str
    create_by: str
    files_name: List[str] = []

class ThreadUpdate(BaseModel):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str

class Thread(ThreadBase):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str

    author: Optional['Author'] = None # type: ignore
    have_file: List['ThreadFiles'] = None # type: ignore
    likes: List['ThreadLiked'] = None # type: ignore
    comments: List['Comment'] = None # type: ignore
    
    class Config:
        from_attributes = True


