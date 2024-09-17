from ..schemas import Thread, ThreadCreate, ThreadBase
from .. import models

from sqlalchemy.orm import Session

def find_by_course_id(db: Session, course_id: str, limit: int, offset: int):
    return db.query(models.Threads).filter(models.Threads.course_id == course_id).limit(limit).offset(offset)

def find_thread(db: Session, thread_id: int):
    return db.query(models.Threads).filter(models.Threads.id == thread_id).first()

def create_thread(db: Session, thread: ThreadCreate):

    db_thread = models.Threads(
        create_by = thread.create_by,
        course_id = thread.course_id,
        title = thread.title,
        body = thread.body,
        is_highlight = thread.is_highlight,
        create_at = thread.create_at
    )
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread
    