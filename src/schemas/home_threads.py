from pydantic import BaseModel
from typing import List, Optional


class HomeThreadBase(BaseModel):
    pass

class HomeThreadCreate(HomeThreadBase):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str
    create_by: str
    files_name: List[str] = None

class HomeThreadUpdate(BaseModel):
    title: str
    body: str
    is_highlight: bool | None = False
    create_at: str

class HomeThreadForStudent(HomeThreadBase):
    title: str
    body: str

class HomeThread(HomeThreadBase):
    id: int
    create_by: str
    title: str
    body: str
    is_highlight: bool | None = False
    likes: int
    create_at: str

    files: List['HomeThreadsFiles'] = None # type: ignore
    liked_by: List['HomeThreadLikedBase'] = None # type: ignore
    comments: List['HomeCommentForThread'] = None # type: ignore
    author: Optional['Student'] = None # type: ignore

    class Config:
        from_attributes = True