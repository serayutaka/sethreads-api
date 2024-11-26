from typing import List, Union
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import jwt

from ...common import get_db
from ...crud import student_helper
from ...schemas import Student, Course, EnrollmentCreate

router = APIRouter(
    prefix="/student",
    tags=["student"],
    responses={404: {"description": "Not found"}}
)

@router.get("/get-info", response_model=Student)
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

@router.get("/get-all", response_model=List[Student])
def read_students(year: str, course_id: str, db: Session = Depends(get_db)):
    db_students = student_helper.get_all(db, year, course_id)
    if db_students == []:
        raise HTTPException(status_code=404, detail="No students found")
    return db_students

@router.put("/update-ta", response_model=Union[Student, dict])
def update_ta(student_id: str, is_ta: bool, ta_course_id: str, db: Session = Depends(get_db), x_token: str = Header(None)):
    decoded_token = jwt.decode(x_token, "mysecretpassword", algorithms=["HS256"])
    if (decoded_token["sub"]["student_id"] != "admin"):
        return { "error": "Unauthorized" }
    
    db_student = student_helper.update_ta(db, student_id, is_ta, ta_course_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if db_student == "Course not found":
        return { "error": "Course not found" }
    if db_student == "First year student cannot be a TA":
        return { "error": "First year student cannot be a TA" }
    if db_student == "TA course year is not allowed":
        return { "error": "TA course year is not allowed" }
    return db_student

@router.post("/register-course", response_model=Union[Student, dict])
def register_course(course: EnrollmentCreate, db: Session = Depends(get_db), x_token: str = Header(None)):
    decoded_token = jwt.decode(x_token, "mysecretpassword", algorithms=["HS256"])
    if (decoded_token["sub"]["student_id"] != "admin"):
        return { "error": "Unauthorized" }
    
    db_student = student_helper.register_course(db, course)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if db_student == "Course not found":
        return { "error": "Course not found" }
    if db_student == "Course already registered":
        return { "error": "Course already registered" }
    if db_student == "Course year is higher than student year":
        return { "error": "First year student cannot register for this course" }
    if db_student == "First year student cannot register for this course":
        return { "error": "First year student cannot register for this course" }
    
    return db_student

@router.delete("/withdraw-course", response_model=Union[Student, dict])
def withdraw_course(student_id: str, course_id: str, db: Session = Depends(get_db), x_token: str = Header(None)):
    decoded_token = jwt.decode(x_token, "mysecretpassword", algorithms=["HS256"])
    if (decoded_token["sub"]["student_id"] != "admin"):
        return { "error": "Unauthorized" }
    
    db_student = student_helper.withdraw_course(db, student_id, course_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    if db_student == "Course not found":
        return { "error": "Course not found" }
    return db_student