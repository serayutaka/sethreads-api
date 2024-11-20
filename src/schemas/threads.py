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
    files_name: List[str] = None

class ThreadUpdate(BaseModel):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str

class ThreadForStudent(ThreadBase):
    id: int
    title: str
    likes: int
    comments: List['CommentForThread'] = None # type: ignore

class Thread(ThreadBase):
    id: int
    create_by: str
    title: str
    body: str
    is_highlight: bool | None = False
    likes: int
    create_at: str

    files: List['ThreadsFiles'] = None # type: ignore
    liked_by: List['ThreadLikedBase'] = None # type: ignore
    comments: List['CommentForThread'] = None # type: ignore
    author: Optional['Student'] = None # type: ignore

    class Config:
        from_attributes = True


