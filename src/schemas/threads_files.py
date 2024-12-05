from pydantic import BaseModel

class ThreadFilesBase(BaseModel):
    id: int

class ThreadFilesCreate(ThreadFilesBase):
    thread_id: int
    file_name: str

class ThreadFiles(ThreadFilesBase):
    thread_id: int
    file_name: str

    class Config:
        orm_mode = True