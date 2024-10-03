from sqlalchemy.orm import Session

from .. import models

def find(db: Session, student_id: str):
    return db.query(models.Students).filter(models.Students.student_id == student_id).first()

def find_courses(db: Session, course_id: str):
    return db.query(models.Courses).filter(models.Courses.course_id == course_id).first()

# def update(db: Session, student: models.Student):
#     db.query(models.Student).filter(models.Student.id == student.id).update(student)
#     db.commit()
#     return student

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