from sqlalchemy.orm import Session

from ..schemas import CommentCreate, SubCommentCreate, CommentUpdate
from .. import models

def find_by_thread_id(db: Session, thread_id: int, limit: int, offset: int):
    count = db.query(models.Comments).filter(models.Comments.comment_from == thread_id).count()
    if count == 0:
        return None
    return db.query(models.Comments).filter(models.Comments.comment_from == thread_id).limit(limit).offset(offset).all()

def update_comment(db: Session, db_comment: models.Comments, comment: CommentUpdate):
    db_comment.comment_data = comment.comment_data
    db_comment.create_at = comment.create_at
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_comment(db: Session, comment: CommentCreate):

    db_comment = models.Comments(
        comment_from = comment.comment_from,
        comment_data = comment.comment_data,
        posted_by = comment.posted_by,
        create_at = comment.create_at
    )

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def find_comment(db: Session, comment_id: int):
    count = db.query(models.Comments).filter(models.Comments.id == comment_id).count()
    if count == 0:
        return None
    return db.query(models.Comments).filter(models.Comments.id == comment_id).first()

def delete_comment(db: Session, comment: models.Comments):
    db.delete(comment)
    db.commit()

def create_subcomment(db: Session, subcomment: SubCommentCreate):
    comment_check = find_comment(db, subcomment.reply_of)
    if comment_check is None:
        return None
    
    db_subcomment = models.SubComments(
        reply_of = subcomment.reply_of,
        posted_by = subcomment.posted_by,
        reply_data = subcomment.reply_data,
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
    db_subcomment.reply_data = subcomment.reply_data
    db_subcomment.create_at = subcomment.create_at
    db.commit()
    db.refresh(db_subcomment)
    return db_subcomment

def delete_subcomment(db: Session, subcomment: models.SubComments):
    db.delete(subcomment)
    db.commit()