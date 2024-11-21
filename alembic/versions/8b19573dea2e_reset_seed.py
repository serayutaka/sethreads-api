"""Reset Seed

Revision ID: 8b19573dea2e
Revises: 66cc4dff37c5
Create Date: 2024-11-21 15:29:14.084875

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b19573dea2e'
down_revision: Union[str, None] = '66cc4dff37c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('courses')
    op.drop_table('threads')
    op.drop_table('home_likes')
    op.drop_table('students')
    op.drop_table('comments')
    op.drop_table('threads_files')
    op.drop_table('home')
    op.drop_table('subcomments')
    op.drop_table('threads_likes')
    op.drop_table('home_comments')
    op.drop_table('home_subcomments')
    op.drop_table('home_files')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('home_files',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('thread_id', sa.INTEGER(), nullable=True),
    sa.Column('file_name', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['home.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('home_subcomments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reply_of', sa.INTEGER(), nullable=True),
    sa.Column('reply_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.VARCHAR(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['reply_of'], ['home_comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('home_comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('comment_from', sa.INTEGER(), nullable=True),
    sa.Column('comment_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.VARCHAR(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['comment_from'], ['home.id'], ),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threads_likes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('thread_id', sa.INTEGER(), nullable=True),
    sa.Column('student_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subcomments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reply_of', sa.INTEGER(), nullable=True),
    sa.Column('reply_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.VARCHAR(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['reply_of'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('home',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('create_by', sa.VARCHAR(), nullable=True),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('body', sa.VARCHAR(), nullable=True),
    sa.Column('is_highlight', sa.BOOLEAN(), nullable=True),
    sa.Column('likes', sa.INTEGER(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['create_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threads_files',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('thread_id', sa.INTEGER(), nullable=True),
    sa.Column('file_name', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['thread_id'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('comment_from', sa.INTEGER(), nullable=True),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('comment_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.VARCHAR(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['comment_from'], ['threads.id'], ),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('student_id', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('surname', sa.VARCHAR(), nullable=True),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.Column('is_ta', sa.BOOLEAN(), nullable=True),
    sa.Column('picture', sa.BLOB(), nullable=True),
    sa.Column('ta_course_id', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('home_likes',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('thread_id', sa.INTEGER(), nullable=True),
    sa.Column('student_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['thread_id'], ['home.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threads',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('create_by', sa.VARCHAR(), nullable=True),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('body', sa.VARCHAR(), nullable=True),
    sa.Column('is_highlight', sa.BOOLEAN(), nullable=True),
    sa.Column('likes', sa.INTEGER(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['create_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('student_id', sa.VARCHAR(), nullable=True),
    sa.Column('year', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
