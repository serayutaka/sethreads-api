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
        likes = 0,
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

def update_thread_highlight(db: Session, db_thread: models.HomeThreads):
    db_thread.is_highlight = not db_thread.is_highlight
    db.commit()
    db.refresh(db_thread)
    return db_thread

def update_thread_likes(db: Session, is_like: bool, db_thread: models.HomeThreads):
    if is_like:
        db_thread.likes += 1
    else:
        if db_thread.likes > 0:
            db_thread.likes -= 1
    db.commit()
    db.refresh(db_thread)
    return db_thread

def delete_thread(db: Session, thread: models.HomeThreads):
    db_comment_of_thread = db.query(models.HomeComments).filter(models.HomeComments.comment_from == thread.id)
    for comment in db_comment_of_thread:
        db.query(models.HomeSubComments).filter(models.HomeSubComments.reply_of == comment.id).delete()
    db_comment_of_thread.delete()
    db.delete(thread)
    db.commit()