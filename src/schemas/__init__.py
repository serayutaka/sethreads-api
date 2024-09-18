from .students import Student, StudentCreate, StudentBase
from .courses import Course, CourseCreate, CourseBase
from .threads import Thread, ThreadCreate, ThreadBase
from .comments import Comment, CommentCreate
from .subcomments import SubComment, SubCommentCreate

Student.model_rebuild()
Course.model_rebuild()
Thread.model_rebuild()
ThreadCreate.model_rebuild()
Comment.model_rebuild()