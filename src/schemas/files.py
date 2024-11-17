from pydantic import BaseModel

class HomeThreadsFiles(BaseModel):
    id: int
    file_name: str

class ThreadsFiles(BaseModel):
    id: int
    file_name: str