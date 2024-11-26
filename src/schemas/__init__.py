from .students import Student, StudentCreate, StudentBase
from .enrollment import Enrollment, EnrollmentBase, EnrollmentCreate
from .course import Course, CourseBase, CourseCreate
from .threads import Thread, ThreadCreate, ThreadBase, ThreadUpdate
from .threads_files import ThreadFiles, ThreadFilesCreate, ThreadFilesBase
from .thread_liked import ThreadLikedBase, ThreadLikedCreate, ThreadLiked
from .threads_comments import Comment, CommentCreate, CommentUpdate
from .subcomments import SubComment, SubCommentCreate, SubCommentUpdate

Student.model_rebuild()
Enrollment.model_rebuild()