from sqlalchemy.orm import Session
import json
from .. import models

with open('src/courses.json') as f:
    courses = json.load(f)

def find(db: Session, student_id: str):
    return db.query(models.Students).filter(models.Students.id == student_id).first()

def find_courses(db: Session, course_id: str):
    return db.query(models.Course).filter(models.Course.id == course_id).first()

def get_all(db: Session, year: str, course_id: str):
    if (year == 'all' and course_id == 'all'):
        return db.query(models.Students).all()
    elif (year != 'all' and course_id == 'all'):
        return db.query(models.Students).filter(models.Students.year == year).all()
    else:
        db_student_year = db.query(models.Students).filter(models.Students.year == year).all()
        
        if not db_student_year:
            return []
        
        students_to_keep = []
        for student in db_student_year:
            courseID = [course.course_id for course in student.registered]
            if course_id in courseID:
                students_to_keep.append(student)
        
        return students_to_keep

def update_ta(db: Session, student_id: str, is_ta: bool, ta_course_id: str):
    db_student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if db_student is None:
        return None
    if is_ta == False:
        db_student.is_ta = False
        db_student.ta_course_id = None
        db.commit()
        db.refresh(db_student)

        return db_student

    if ta_course_id not in courses:
        return "Course not found"
    if db_student.year == 1:
        return "First year student cannot be a TA"
    if ta_course_id[0:3] == "010":
        pass
    elif ta_course_id[5] >= str(db_student.year):
        return "TA course year is not allowed"

    db_student.is_ta = is_ta
    db_student.ta_course_id = ta_course_id
    db.commit()
    db.refresh(db_student)
    return db_student

def register_course(db: Session, course):
    db_student = db.query(models.Students).filter(models.Students.id == course.student_id).first()
    if db_student is None:
        return None
    if course.course_id not in courses:
        return "Course not found"
    for reg_course in db_student.registered:
        if reg_course.course_id == course.course_id:
            return "Course already registered"
        
    if course.course_id[0:3] == "012" and course.course_id[5] > str(db_student.year):
        return "Course year is higher than student year"
    
    if db_student.year == 1 and course.course_id == "01006719":
        return "First year student cannot register for this course"
    
    enroll = models.Enrollment(
        course_id = course.course_id,
        student_id = course.student_id,
    )
    
    db.add(enroll)
    db.commit()
    db.refresh(enroll)
    return db_student

def withdraw_course(db: Session, student_id: str, course_id: str):
    db_student = db.query(models.Students).filter(models.Students.id == student_id).first()
    if db_student is None:
        return None
    if course_id not in courses:
        return "Course not found"
    enrollment = db.query(models.Enrollment).filter(
        models.Enrollment.course_id == course_id,
        models.Enrollment.student_id == student_id
    ).first()
    
    db.delete(enrollment)
    db.commit()
    db.refresh(db_student)
    return db_student