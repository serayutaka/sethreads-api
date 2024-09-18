from .students import Student, StudentCreate, StudentBase, StudentAllAttributes
from .courses import Course, CourseCreate, CourseBase
from .threads import Thread, ThreadCreate, ThreadBase, ThreadUpdate, ThreadForStudent
from .comments import Comment, CommentCreate, CommentUpdate, CommentForStudent
from .subcomments import SubComment, SubCommentCreate, SubCommentUpdate, SubCommentForStudent

Student.model_rebuild()
StudentAllAttributes.model_rebuild()



Course.model_rebuild()
Thread.model_rebuild()
ThreadCreate.model_rebuild()
Comment.model_rebuild()