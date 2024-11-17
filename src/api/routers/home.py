from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
import mimetypes
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from ...common import get_db, send_emails
from ...crud import home_helper, student_helper
from ...schemas import HomeThread, HomeThreadCreate, HomeThreadUpdate
from config.settings import UPLOAD_DIRICTORY

router = APIRouter(
    prefix="/home",
    tags=["home"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-all", response_model=list[HomeThread])
def read_home_threads(limit: int, offset: int, db: Session = Depends(get_db)):
    db_threads = home_helper.find_all(db, limit, offset)
    if db_threads is None:
        raise HTTPException(status_code=404, detail="No threads found")
    elif db_threads == []:
        return []
    return db_threads

@router.get("/get-thread", response_model=HomeThread)
def read_home_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_thread

@router.post("/upload-files")
async def create_upload_file(files: List[UploadFile]):
    result = await home_helper.save_files(files, UPLOAD_DIRICTORY)
    if (result != True):
        raise HTTPException(status_code=500, detail="Failed to save file")
    return {"message": "File uploaded successfully"}

@router.get("/get-file", response_class=FileResponse)
def download_file(file_name: str, thread_id: str):
    file_name = f"homeID_{thread_id}-{file_name}"
    file_path = UPLOAD_DIRICTORY / file_name
    if not file_path.exists:
        raise HTTPException(status_code=404, detail="File not found")
    
    media_type, _ = mimetypes.guess_type(str(file_path))
    if media_type is None:
        media_type = "application/octet-stream"
    return FileResponse(path=file_path, media_type=media_type, filename=file_name)

@router.post("/create-thread", response_model=HomeThread, status_code=201)
async def create_home_thread(thread: HomeThreadCreate, notify: bool, db: Session = Depends(get_db)):
    try:
        db_thread = home_helper.create_thread(db, thread)
        db.refresh(db_thread, ["author"])

        # Send email to all students
        """ This is a code where when we get domain name
        students = student_helper.find_all(db)
        recipants_emails = [f"{student.student_id}@kmitl.ac.th" for student in students]
        recipants_name = [student.name for student in students]
        """
        
        if notify:
            recipants_student_id = ["66011192"]
            recipants_emails = [f"{student_id}@kmitl.ac.th" for student_id in recipants_student_id]
            recipants_name = [student_helper.find(db, student_id).name for student_id in recipants_student_id]
            recipants = dict(zip(recipants_name, recipants_emails))
            title = BeautifulSoup(db_thread.title, "html.parser").get_text()
            thread_url = f"http://localhost:3000/home/thread/{db_thread.id}"

            await send_emails(db_thread.author.name, recipants, title, thread_url)

        return db_thread
    except Exception as e:
        return e
    
@router.put("/update-thread", response_model=HomeThreadUpdate)
def update_home_thread(thread_id: int, thread: HomeThreadUpdate, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return home_helper.update_thread(db, db_thread, thread)

@router.put("/update-is-highlight", response_model=HomeThreadUpdate)
def update_home_thread_highlight(thread_id: int, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return home_helper.update_thread_highlight(db, db_thread)

class LikeThreads(BaseModel):
    thread_id: int
    student_id: str
    is_like: bool

@router.put("/update-likes")
def update_home_thread_likes(likeThreads: LikeThreads, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, likeThreads.thread_id)
    db_thread_like = home_helper.find_student_liked_thread(db, likeThreads.thread_id, likeThreads.student_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    elif db_thread_like.first() is None and likeThreads.is_like == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    elif db_thread_like.first() is not None and likeThreads.is_like == True:
        raise HTTPException(status_code=403, detail="Forbidden")
    return home_helper.update_thread_likes(db, likeThreads.student_id, likeThreads.is_like, db_thread, db_thread_like).likes

@router.delete("/delete-thread")
def delete_home_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    home_helper.delete_thread(db, db_thread)
    return {"message": "Thread deleted successfully"}