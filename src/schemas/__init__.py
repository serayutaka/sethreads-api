from .students import Student, StudentCreate, StudentBase, StudentAllAttributes
from .courses import Course, CourseCreate, CourseBase
from .threads import Thread, ThreadCreate, ThreadBase, ThreadUpdate, ThreadForStudent
from .comments import Comment, CommentCreate, CommentUpdate, CommentForStudent, CommentForThread
from .subcomments import SubComment, SubCommentCreate, SubCommentUpdate, SubCommentForStudent
from .home_threads import HomeThread, HomeThreadCreate, HomeThreadBase, HomeThreadUpdate, HomeThreadForStudent
from .home_comments import HomeCommentForThread, HomeCommentForStudent, HomeComment, HomeCommentCreate, HomeCommentUpdate
from .home_subcomments import HomeSubComment, HomeSubCommentCreate, HomeSubCommentUpdate, HomeSubCommentForStudent

Student.model_rebuild()
StudentAllAttributes.model_rebuild()
Course.model_rebuild()
Thread.model_rebuild()
ThreadCreate.model_rebuild()
Comment.model_rebuild()
HomeThread.model_rebuild()
HomeComment.model_rebuild()
HomeSubComment.model_rebuild()