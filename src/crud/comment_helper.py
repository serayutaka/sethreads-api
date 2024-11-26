from sqlalchemy.orm import Session

from ..schemas import CommentCreate, SubCommentCreate, CommentUpdate
from .. import models

def find_by_thread_id(db: Session, thread_id: int, limit: int, offset: int):
    check_thread = db.query(models.Threads).filter(models.Threads.id == thread_id).count()
    if check_thread == 0:
        return None
    
    count = db.query(models.ThreadsComments).filter(models.ThreadsComments.thread_id == thread_id).count()
    if count == 0:
        return []
    return db.query(models.ThreadsComments).filter(models.ThreadsComments.thread_id == thread_id).limit(limit).offset(offset).all()

def find_last_comment(db: Session, thread_id: int):
    check_thread = db.query(models.Threads).filter(models.Threads.id == thread_id).count()
    if check_thread == 0:
        return None

    count = db.query(models.ThreadsComments).filter(models.ThreadsComments.thread_id == thread_id).count()
    if count == 0:
        return None
    
    return db.query(models.ThreadsComments).filter(models.ThreadsComments.thread_id == thread_id).order_by(models.ThreadsComments.id.desc()).first()

def update_comment(db: Session, db_comment: models.ThreadsComments, comment: CommentUpdate):
    db_comment.body = comment.body
    db_comment.create_at = comment.create_at
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_comment(db: Session, comment: CommentCreate):

    db_comment = models.ThreadsComments(
        thread_id = comment.thread_id,
        course_id = comment.course_id,
        body = comment.body,
        commented_by = comment.commented_by,
        create_at = comment.create_at
   )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def find_comment(db: Session, comment_id: int):
    count = db.query(models.ThreadsComments).filter(models.ThreadsComments.id == comment_id).count()
    if count == 0:
        return None
    return db.query(models.ThreadsComments).filter(models.ThreadsComments.id == comment_id).first()

def delete_comment(db: Session, comment: models.ThreadsComments):
    db.delete(comment)
    db.commit()

def create_subcomment(db: Session, subcomment: SubCommentCreate):
    comment_check = find_comment(db, subcomment.comment_id)
    if comment_check is None:
        return None
    
    db_subcomment = models.SubComments(
        comment_id = subcomment.comment_id,
        replied_by = subcomment.replied_by,
        body = subcomment.body,
        create_at = subcomment.create_at
    )

    db.add(db_subcomment)
    db.commit()
    db.refresh(db_subcomment)
    return db_subcomment

def find_subcomment(db: Session, subcomment_id: int):
    count = db.query(models.SubComments).filter(models.SubComments.id == subcomment_id).count()
    if count == 0:
        return None
    return db.query(models.SubComments).filter(models.SubComments.id == subcomment_id).first()

def update_subcomment(db: Session, db_subcomment: models.SubComments, subcomment: SubCommentCreate):
    db_subcomment.body = subcomment.body
    db_subcomment.create_at = subcomment.create_at
    db.commit()
    db.refresh(db_subcomment)
    return db_subcomment

def delete_subcomment(db: Session, subcomment: models.SubComments):
    db.delete(subcomment)
    db.commit()