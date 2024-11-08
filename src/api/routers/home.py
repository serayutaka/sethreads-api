from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ...common import get_db
from ...crud import home_helper
from ...schemas import HomeThread, HomeThreadCreate, HomeThreadUpdate

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

@router.post("/create-thread", response_model=HomeThread, status_code=201)
def create_home_thread(thread: HomeThreadCreate, db: Session = Depends(get_db)):
    try:
        db_thread = home_helper.create_thread(db, thread)
        db.refresh(db_thread, ["author"])
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