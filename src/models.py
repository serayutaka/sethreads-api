from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Students(Base):
    __tablename__ = "students"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String)
    surname = Column(String)
    hashed_password = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    is_ta = Column(Boolean, nullable=True)
    picture = Column(LargeBinary, nullable=True)
    ta_course_id = Column(String, nullable=True)

    registered = relationship("Enrollment", cascade="all, delete")
    posted = relationship("Threads", back_populates="author")
    liked = relationship("ThreadsLikes", cascade="all, delete")
    comment = relationship("ThreadsComments", cascade="all, delete")
    reply = relationship("SubComments", cascade="all, delete")

class Enrollment(Base):
    __tablename__ = "enrollment"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("course.id"))
    student_id = Column(String, ForeignKey("students.id"))

    course = relationship("Course", cascade="all, delete")

class Course(Base):
    __tablename__ = "course"
    id = Column(String, primary_key=True, unique=True)
    name = Column(String)
    require_year = Column(Integer)

class Threads(Base):
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String)
    body = Column(String)
    is_highlight = Column(Boolean)
    create_at = Column(String)
    create_by = Column(String, ForeignKey("students.id"))
    course_id = Column(String, ForeignKey("course.id"))
    
    author = relationship("Students", back_populates="posted")
    have_file = relationship("ThreadsFiles", cascade="all, delete")
    likes = relationship("ThreadsLikes", cascade="all, delete")
    comments = relationship("ThreadsComments", cascade="all, delete")

class ThreadsFiles(Base):
    __tablename__ = "threads_files"
    id = Column(Integer, primary_key=True, autoincrement=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    file_name = Column(String)

class ThreadsLikes(Base):
    __tablename__ = "threads_likes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(String, ForeignKey("course.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"))
    student_id = Column(String, ForeignKey("students.id"))

class ThreadsComments(Base):
    __tablename__ = "threads_comments"

    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey("threads.id"))
    course_id = Column(String, ForeignKey("course.id"))
    body = Column(String)
    commented_by = Column(String, ForeignKey("students.id"))
    create_at = Column(String)

    replies = relationship("SubComments", cascade="all, delete")
    author = relationship("Students", back_populates="comment")

class SubComments(Base):
    __tablename__ = "subcomments"

    id = Column(Integer, primary_key=True)
    comment_id = Column(Integer, ForeignKey("threads_comments.id"))
    body = Column(String)
    replied_by = Column(String, ForeignKey("students.id"))
    create_at = Column(String)
    
    author = relationship("Students", back_populates="reply")