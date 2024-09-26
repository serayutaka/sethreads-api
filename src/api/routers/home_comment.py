from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...common import get_db
from ...crud import home_comment_helper
from ...schemas import HomeComment, HomeCommentCreate, HomeCommentUpdate, HomeSubComment, HomeSubCommentCreate, HomeSubCommentUpdate

router = APIRouter(
    prefix="/home-comment",
    tags=["home-comment"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-all", response_model=list[HomeComment])
def read_home_comments_by_id(home_id: int, limit: int, offset: int, db: Session = Depends(get_db)):
    db_comments = home_comment_helper.find_by_id(db, home_id, limit, offset)
    if db_comments is None:
        raise HTTPException(status_code=404, detail="No comments found")
    return db_comments

@router.put("/update-comment", response_model=HomeComment)
def update_home_comment(comment_id: int, comment: HomeCommentUpdate, db: Session = Depends(get_db)):
    db_comment = home_comment_helper.find_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return home_comment_helper.update_comment(db, db_comment, comment)

@router.post("/create-comment", response_model=HomeComment, status_code=201)
def create_home_comment(comment: HomeCommentCreate, db: Session = Depends(get_db)):
    db_comment =  home_comment_helper.create_comment(db, comment)
    db.refresh(db_comment, ['subcomments', 'author'])
    return db_comment

@router.delete("/delete-comment")
def delete_home_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = home_comment_helper.find_comment(db, comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    home_comment_helper.delete_comment(db, db_comment)
    return {"message": "Comment deleted successfully"}

@router.post("/create-subcomment", response_model=HomeSubComment, status_code=201)
def create_home_subcomment(subcomment: HomeSubCommentCreate, db: Session = Depends(get_db)):
    db_comment = home_comment_helper.find_comment(db, subcomment.reply_of)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return home_comment_helper.create_subcomment(db, subcomment)

@router.put("/update-subcomment", response_model=HomeSubComment)
def update_home_subcomment(subcomment_id: int, subcomment: HomeSubCommentUpdate, db: Session = Depends(get_db)):
    db_subcomment = home_comment_helper.find_subcomment(db, subcomment_id)
    if db_subcomment is None:
        raise HTTPException(status_code=404, detail="Subcomment not found")
    return home_comment_helper.update_subcomment(db, db_subcomment, subcomment)

@router.delete("/delete-subcomment")
def delete_home_subcomment(subcomment_id: int, db: Session = Depends(get_db)):
    db_subcomment = home_comment_helper.find_subcomment(db, subcomment_id)
    if db_subcomment is None:
        raise HTTPException(status_code=404, detail="Subcomment not found")
    home_comment_helper.delete_subcomment(db, db_subcomment)
    return {"message": "Subcomment deleted successfully"}