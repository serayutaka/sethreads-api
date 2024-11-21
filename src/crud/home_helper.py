from fastapi import UploadFile
from typing import List
from pathlib import Path
from ..schemas import HomeThread, HomeThreadCreate, HomeThreadUpdate
from .. import models
import os

from sqlalchemy.orm import Session
from sqlalchemy import and_
from config.settings import UPLOAD_DIRICTORY

def get_all(db: Session):
    count = db.query(models.HomeThreads).count()
    if count == 0:
        return []
    return db.query(models.HomeThreads).all()

def find_all(db: Session, limit: int, offset: int):
    count = db.query(models.HomeThreads).count()
    if count == 0:
        return []
    return db.query(models.HomeThreads).limit(limit).offset(offset)

def find_thread(db: Session, thread_id: int):
    return db.query(models.HomeThreads).filter(models.HomeThreads.id == thread_id).first()

def find_student_liked_thread(db: Session, thread_id: int, student_id: str):
    return db.query(models.HomeThreadsLike).filter(
        and_(
            models.HomeThreadsLike.thread_id == thread_id,
            models.HomeThreadsLike.student_id == student_id
        )
    )

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

    if thread.files_name:
        for file_name in thread.files_name:
            create_home_thread_file(db, db_thread.id, file_name)
    
    return db_thread

def create_home_thread_file(db: Session, thread_id: int, file_name: str):
    db_thread_file = models.HomeThreadsFiles(
        thread_id = thread_id,
        file_name = file_name
    )
    db.add(db_thread_file)
    db.commit()
    db.refresh(db_thread_file)
    return db_thread_file

async def save_files(files: List[UploadFile], save_path: Path):
    for file in files:
        file_path = save_path / file.filename
        try:
            with file_path.open("wb") as buffer:
                buffer.write(file.file.read())
        except Exception as e:
            return e
        finally:
            file.file.close()
    return True
        

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

def update_thread_likes(db: Session, student_id: str, is_like: bool, db_thread: models.HomeThreads, db_thread_like: models.HomeThreadsLike):
    if is_like:
        student_liked = models.HomeThreadsLike(
            thread_id = db_thread.id,
            student_id = student_id
        )
        db.add(student_liked)
        db_thread.likes += 1
    else:
        if db_thread.likes > 0:
            db_thread.likes -= 1
            db_thread_like.delete()
    db.commit()
    db.refresh(db_thread)
    return db_thread

def delete_thread(db: Session, thread: models.HomeThreads):
    db_comment_of_thread = db.query(models.HomeComments).filter(models.HomeComments.comment_from == thread.id)
    for comment in db_comment_of_thread:
        db.query(models.HomeSubComments).filter(models.HomeSubComments.reply_of == comment.id).delete()
    db_comment_of_thread.delete()

    db.query(models.HomeThreadsLike).filter(models.HomeThreadsLike.thread_id == thread.id).delete()

    db_files = db.query(models.HomeThreadsFiles).filter(models.HomeThreadsFiles.thread_id == thread.id)
    for file in db_files:
        filename = f"homeID_{thread.id}-{file.file_name}"
        os.remove(UPLOAD_DIRICTORY / filename)

    db_files.delete()
    db.delete(thread)
    db.commit()