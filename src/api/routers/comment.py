from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...common import get_db
from ...crud import comment_helper
from ...schemas import Comment, CommentCreate, CommentUpdate, SubComment, SubCommentCreate, SubCommentUpdate

router = APIRouter(
    prefix="/comment",
    tags=["comment"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-comments", response_model=list[Comment])
def read_comments_by_thread_id(thread_id: int, limit: int, offset: int, db: Session = Depends(get_db)):
    db_comments = comment_helper.find_by_thread_id(db, thread_id, limit, offset)
    if db_comments is None:
        raise HTTPException(status_code=404, detail="Thread not found")
    return db_comments

@router.put("/update-comment", response_model=Comment)
def update_comment(comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)):
    db_comment = comment_helper.find_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment_helper.update_comment(db, db_comment, comment)

@router.post("/create-comment", response_model=Comment)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment =  comment_helper.create_comment(db, comment)
    db.refresh(db_comment, ['subcomments', 'author'])
    return db_comment

@router.delete("/delete-comment")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = comment_helper.find_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    comment_helper.delete_comment(db, db_comment)
    return {"message": "Comment deleted successfully"}

@router.post("/create-subcomment", response_model=SubComment)
def create_subcomment(subcomment: SubCommentCreate, db: Session = Depends(get_db)):
    return comment_helper.create_subcomment(db, subcomment)

@router.put("/update-subcomment", response_model=SubComment)
def update_subcomment(subcomment_id: int, subcomment: SubCommentUpdate, db: Session = Depends(get_db)):
    db_subcomment = comment_helper.find_subcomment(db, subcomment_id)
    if db_subcomment is None:
        raise HTTPException(status_code=404, detail="Subcomment not found")
    return comment_helper.update_subcomment(db, db_subcomment, subcomment)

@router.delete("/delete-subcomment")
def delete_subcomment(subcomment_id: int, db: Session = Depends(get_db)):
    db_subcomment = comment_helper.find_subcomment(db, subcomment_id)
    if db_subcomment is None:
        raise HTTPException(status_code=404, detail="Subcomment not found")
    comment_helper.delete_subcomment(db, db_subcomment)
    return {"message": "Subcomment deleted successfully"}