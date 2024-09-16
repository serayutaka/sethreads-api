from sqlalchemy.orm import Session

from .. import models

def find(db: Session, student_id: str):
    return db.query(models.Students).filter(models.Students.student_id == student_id).first()

def find_courses(db: Session, course_id: str):
    return db.query(models.Courses).filter(models.Courses.id == course_id).first()

# def update(db: Session, student: models.Student):
#     db.query(models.Student).filter(models.Student.id == student.id).update(student)
#     db.commit()
#     return student