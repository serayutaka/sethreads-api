from ..schemas import Thread, ThreadCreate, ThreadBase, ThreadUpdate
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

def update_thread(db: Session, db_thread: models.Threads, thread: ThreadUpdate):
    db_thread.title = thread.title
    db_thread.body = thread.body
    db_thread.is_highlight = thread.is_highlight
    db_thread.create_at = thread.create_at
    db.commit()
    db.refresh(db_thread)
    return db_thread

def delete_thread(db: Session, thread: models.Threads):
    db.delete(thread)
    db.commit()
