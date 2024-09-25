from sqlalchemy.orm import Session

from .. import models
from ..schemas import HomeCommentCreate, HomeCommentUpdate, HomeSubCommentCreate, HomeSubCommentUpdate

def find_by_id(db: Session, home_id: int, limit: int, offset: int):
    count = db.query(models.HomeComments).filter(models.HomeComments.comment_from == home_id).count()
    if count == 0:
        return None
    return db.query(models.HomeComments).filter(models.HomeComments.comment_from == home_id).limit(limit).offset(offset).all()

def update_comment(db: Session, db_comment: models.HomeComments, comment: HomeCommentUpdate):
    db_comment.comment_data = comment.comment_data
    db_comment.create_at = comment.create_at
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_comment(db: Session, comment: HomeCommentCreate):
    
    db_comment = models.HomeComments(
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
    count = db.query(models.HomeComments).filter(models.HomeComments.id == comment_id).count()
    if count == 0:
        return None
    return db.query(models.HomeComments).filter(models.HomeComments.id == comment_id).first()

def delete_comment(db: Session, comment: models.HomeComments):
    db.delete(comment)
    db.commit()

def create_subcomment(db: Session, subcomment: HomeSubCommentCreate):
    comment_check = find_comment(db, subcomment.reply_of)
    if comment_check is None:
        return None
    
    db_subcomment = models.HomeSubComments(
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
    count = db.query(models.HomeSubComments).filter(models.HomeSubComments.id == subcomment_id).count()
    if count == 0:
        return None
    return db.query(models.HomeSubComments).filter(models.HomeSubComments.id == subcomment_id).first()

def update_subcomment(db: Session, db_subcomment: models.HomeSubComments, subcomment: HomeSubCommentUpdate):
    db_subcomment.reply_data = subcomment.reply_data
    db_subcomment.create_at = subcomment.create_at
    db.commit()
    db.refresh(db_subcomment)
    return db_subcomment

def delete_subcomment(db: Session, subcomment: models.HomeSubComments):
    db.delete(subcomment)
    db.commit()
