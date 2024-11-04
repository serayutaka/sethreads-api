from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from ...common import get_db
from ...crud import thread_helper
from ...schemas import Thread, ThreadCreate, ThreadUpdate

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

@router.post("/create-thread", response_model=Thread, status_code=201)
def create_thread(thread: ThreadCreate, db: Session = Depends(get_db)):
    try:
        db_thread = thread_helper.create_thread(db, thread)
        db.refresh(db_thread, ["author"])
        return db_thread
    except Exception as e:
        return e

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

@router.put("/update-likes")
def update_thread_likes(thread_id: int, student_id: str, is_like: bool, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    db_thread_like = thread_helper.find_student_liked_thread(db, thread_id, student_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    elif db_thread_like.first() is None and is_like == False:
        raise HTTPException(status_code=403, detail="Forbidden")
    elif db_thread_like.first() is not None and is_like == True:
        raise HTTPException(status_code=403, detail="Forbidden")
    return thread_helper.update_thread_likes(db, is_like, student_id, db_thread, db_thread_like)

@router.delete("/delete-thread")
def delete_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = thread_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    thread_helper.delete_thread(db, db_thread)
    return {"message": "Thread deleted successfully"}