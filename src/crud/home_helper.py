from ..schemas import HomeThread, HomeThreadCreate, HomeThreadUpdate
from .. import models

from sqlalchemy.orm import Session

def find_all(db: Session, limit: int, offset: int):
    count = db.query(models.HomeThreads).count()
    if count == 0:
        return []
    return db.query(models.HomeThreads).limit(limit).offset(offset)

def find_thread(db: Session, thread_id: int):
    return db.query(models.HomeThreads).filter(models.HomeThreads.id == thread_id).first()

def create_thread(db: Session, thread: HomeThreadCreate):
    db_thread = models.HomeThreads(
        create_by = thread.create_by,
        title = thread.title,
        body = thread.body,
        is_highlight = thread.is_highlight,
        create_at = thread.create_at
    )
    db.add(db_thread)
    db.commit()
    db.refresh(db_thread)
    return db_thread

def update_thread(db: Session, db_thread: models.HomeThreads, thread: HomeThreadUpdate):
    db_thread.title = thread.title
    db_thread.body = thread.body
    db_thread.is_highlight = thread.is_highlight
    db_thread.create_at = thread.create_at
    db.commit()
    db.refresh(db_thread)
    return db_thread

def delete_thread(db: Session, thread: models.HomeThreads):
    db.delete(thread)
    db.commit()