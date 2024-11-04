from ..schemas import Thread, ThreadCreate, ThreadBase, ThreadUpdate, Course
from .. import models

from sqlalchemy.orm import Session
from sqlalchemy import and_

def find_by_course_id(db: Session, course_id: str, limit: int, offset: int):
    is_valid_course_id = db.query(models.Courses).filter(models.Courses.course_id == course_id).count()
    if is_valid_course_id == 0:
        print("t")
        return None
    else:
        count = db.query(models.Threads).filter(models.Threads.course_id == course_id).count()
        if count == 0:
            return []
        return db.query(models.Threads).filter(models.Threads.course_id == course_id).limit(limit).offset(offset)

def find_thread(db: Session, thread_id: int, course_id: str = None):
    if course_id is None:
        return db.query(models.Threads).filter(models.Threads.id == thread_id).first()

    is_valid = db.query(models.Threads).filter(
            models.Threads.id == thread_id,
            models.Threads.course_id == course_id
    ).count()
    if is_valid == 0:
        return None
    return db.query(models.Threads).filter(models.Threads.id == thread_id).first()

def create_thread(db: Session, thread: ThreadCreate):

    db_thread = models.Threads(
        create_by = thread.create_by,
        course_id = str(thread.course_id),
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

def update_thread(db: Session, db_thread: models.Threads, thread: ThreadUpdate):
    db_thread.title = thread.title
    db_thread.body = thread.body
    db_thread.is_highlight = thread.is_highlight
    db_thread.create_at = thread.create_at
    db.commit()
    db.refresh(db_thread)
    return db_thread

def delete_thread(db: Session, thread: models.Threads):
    db_comment_of_thread = db.query(models.Comments).filter(models.Comments.comment_from == thread.id)
    for comment in db_comment_of_thread:
        db.query(models.SubComments).filter(models.SubComments.reply_of == comment.id).delete()
    db_comment_of_thread.delete()
    db.delete(thread)
    db.commit()

def update_thread_highlight(db: Session, db_thread: models.Threads):
    db_thread.is_highlight = not db_thread.is_highlight
    db.commit()
    db.refresh(db_thread)
    return db_thread