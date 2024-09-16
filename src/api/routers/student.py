from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session

from ...database import SessionLocal
from ...crud import student_helper
from ...dependencies import verify_token
from ...schemas import Student, Course

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/get-info", response_model=Student)
def read_student(student_id: str, db: Session = Depends(get_db)):
    db_student = student_helper.find(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/get-courses", response_model=Course)
def read_ta_courses(course_id: str, db: Session = Depends(get_db)):
    return student_helper.find_courses(db, course_id)

# @router.put("/update-info", response_model=Student)
# def update_student(student: Student, db: Session = Depends(get_db)):
#     return student_helper.update(db, student)