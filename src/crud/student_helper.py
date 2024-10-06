from sqlalchemy.orm import Session
import json
from .. import models

with open('src/courses.json') as f:
    courses = json.load(f)

def find(db: Session, student_id: str):
    return db.query(models.Students).filter(models.Students.student_id == student_id).first()

def find_courses(db: Session, course_id: str):
    return db.query(models.Courses).filter(models.Courses.course_id == course_id).first()

def get_all(db: Session, year: str, course_id: str):
    if (year == 'all' and course_id == 'all'):
        return db.query(models.Students).all()
    elif (year != 'all' and course_id == 'all'):
        return db.query(models.Students).filter(models.Students.year == year).all()
    else:
        db_student_year = db.query(models.Students).filter(models.Students.year == year).all()
        if db_student_year is None:
            return []
        for student in db_student_year:
            courseID = []
            for course in student.registered_courses:
                courseID.append(course.course_id)
            if course_id not in courseID:
                db_student_year.remove(student)
        return db_student_year

def update_ta(db: Session, student_id: str, is_ta: bool, ta_course_id: str):
    db_student = db.query(models.Students).filter(models.Students.student_id == student_id).first()
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
    if ta_course_id[5] > str(db_student.year):
        return "TA course year is higher than student year"

    db_student.is_ta = is_ta
    db_student.ta_course_id = ta_course_id
    db.commit()
    db.refresh(db_student)
    return db_student

def register_course(db: Session, course):
    db_student = db.query(models.Students).filter(models.Students.student_id == course.student_id).first()
    if db_student is None:
        return None
    if course.course_id not in courses:
        return "Course not found"
    for reg_course in db_student.registered_courses:
        if reg_course.course_id == course.course_id:
            return "Course already registered"
    
    create_course = models.Courses(
        course_id = course.course_id,
        name = courses[course.course_id],
        student_id = course.student_id,
        year = course.year
    )
    
    db.add(create_course)
    db.commit()
    db.refresh(create_course)
    return db_student