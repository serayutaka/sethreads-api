from pydantic import BaseModel
from typing import List, Optional

class ThreadBase(BaseModel):
    id: int

class ThreadCreate(ThreadBase):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str
    create_by: str
    files_name: List[str] = None

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

    author: Optional['Student'] = None # type: ignore
    have_files: List['ThreadFiles'] = None # type: ignore
    likes: List['ThreadLiked'] = None # type: ignore
    comments: List['Comment'] = None # type: ignore
    
    class Config:
        from_attributes = True


