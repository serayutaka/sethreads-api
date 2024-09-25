from fastapi import APIRouter, Depends, HTTPException
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

@router.delete("/delete-thread")
def delete_home_thread(thread_id: int, db: Session = Depends(get_db)):
    db_thread = home_helper.find_thread(db, thread_id)
    if db_thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    home_helper.delete_thread(db, db_thread)
    return {"message": "Thread deleted successfully"}