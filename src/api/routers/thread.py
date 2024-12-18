from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from typing import List
from pydantic import BaseModel
import mimetypes
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from bs4 import BeautifulSoup

from ...common import get_db, send_emails
from ...crud import thread_helper, student_helper
from ...schemas import Thread, ThreadCreate, ThreadUpdate
from config.settings import UPLOAD_DIRICTORY

load_dotenv()
router = APIRouter(
    prefix="/thread",
    tags=["thread"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-all", response_model=list[Thread])
def read_threads_by_course_id(course_id: str, limit: int, offset: int, db: Session = Depends(get_db)):
    db_threads = thread_helper.find_by_course_id(db, course_id, limit, offset)
    if db_threads is None:
        raise HTTPException(status_code=404, detail="Course not found")
    elif db_threads == []:
        return []
    return db_threads

@router.get("/get-thread", response_model=Thread)
def read_thread(thread_id: int, course_id: str, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id, course_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_thread

@router.get("/get-title")
def read_thread_title(thread_id: int, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_thread.title

@router.post("/upload-files")
async def create_upload_file(files: List[UploadFile]):
    result = await thread_helper.save_files(files, UPLOAD_DIRICTORY)
    if (result != True):
        raise HTTPException(status_code=500, detail="Failed to save file")
    return {"message": "File uploaded successfully"}

@router.get("/get-file", response_class=FileResponse)
def download_file(file_name: str, thread_id: str):
    file_name = f"threadID_{thread_id}-{file_name}"
    file_path = UPLOAD_DIRICTORY / file_name
    if not file_path.exists:
        raise HTTPException(status_code=404, detail="File not found")
    
    media_type, _ = mimetypes.guess_type(str(file_path))
    if media_type is None:
        media_type = "application/octet-stream"
    return FileResponse(path=file_path, media_type=media_type, filename=file_name)

@router.post("/create-thread", response_model=Thread, status_code=201)
async def create_thread(thread: ThreadCreate, notify: bool, db: Session = Depends(get_db)):
    try:
        db_thread = thread_helper.create_thread(db, thread)
        db.refresh(db_thread, ["author"])

        # Send email to all students in the course
        """ This is a code where when we get domain name
        students = student_helper.get_all(db, db_thread.course_id)
        recipants_emails = [f"{student.student_id}@kmitl.ac.th" for student in students]
        recipants_name = [student.name for student in students]
        """

        if notify:
            recipants_student_id = ["66011192"] # If having the domain, we can get all students id in the course
            recipants_emails = [f"{student_id}@kmitl.ac.th" for student_id in recipants_student_id]
            recipants_name = [student_helper.find(db, student_id).name for student_id in recipants_student_id]
            recipants = dict(zip(recipants_name, recipants_emails))
            title = BeautifulSoup(db_thread.title, "html.parser").get_text()
            thread_url = f"http://localhost:3000/course/{db_thread.course_id}/thread/{db_thread.id}"
            
            await send_emails(db_thread.author.name, recipants, title, thread_url)

        return db_thread
    except Exception as e:
        print(f"Error: {e}")

@router.put("/update-thread", response_model=ThreadUpdate)
def update_thread(thread_id: int, thread: ThreadUpdate, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread_helper.update_thread(db, db_thread, thread)

@router.put("/update-is-highlight", response_model=ThreadUpdate)
def update_thread_highlight(thread_id: int, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return thread_helper.update_thread_highlight(db, db_thread)

class LikeThreads(BaseModel):
    thread_id: int
    student_id: str
    is_like: bool

@router.put("/update-likes")
def update_thread_likes(likeThreads: LikeThreads, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, likeThreads.thread_id)
    db_thread_like = thread_helper.find_student_liked_thread(db, likeThreads.thread_id, likeThreads.student_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    elif db_thread_like.first() is None and likeThreads.is_like == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    elif db_thread_like.first() is not None and likeThreads.is_like == True:
        raise HTTPException(status_code=403, detail="Forbidden")
    return thread_helper.update_thread_likes(db, likeThreads.is_like, likeThreads.student_id, db_thread, db_thread_like).likes

@router.delete("/delete-thread")
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    thread_helper.delete_thread(db, db_thread)
    return {"message": "Thread deleted successfully"}