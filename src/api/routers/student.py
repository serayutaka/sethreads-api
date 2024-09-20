from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session

from ...common import get_db
from ...crud import student_helper
from ...schemas import Student, Course, StudentAllAttributes

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-info", response_model=StudentAllAttributes)
def read_student(student_id: str, db: Session = Depends(get_db)):
    db_student = student_helper.find(db, student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

@router.get("/get-courses", response_model=Course)
def read_ta_courses(course_id: str, db: Session = Depends(get_db)):
    db_ta_course = student_helper.find_courses(db, course_id)
    if db_ta_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_ta_course

# @router.put("/update-info", response_model=Student)
# def update_student(student: Student, db: Session = Depends(get_db)):
#     return student_helper.update(db, student)