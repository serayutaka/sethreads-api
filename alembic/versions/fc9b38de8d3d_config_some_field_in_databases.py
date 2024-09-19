"""Config some field in databases

Revision ID: fc9b38de8d3d
Revises: 1cec35371cfa
Create Date: 2024-09-18 14:41:29.191177

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fc9b38de8d3d'
down_revision: Union[str, None] = '1cec35371cfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subcomments')
    op.drop_table('courses')
    op.drop_table('threads_pictures')
    op.drop_table('comments_pictures')
    op.drop_table('comments')
    op.drop_table('threads')
    op.drop_table('students')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    op.create_table('threads',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('create_by', sa.VARCHAR(), nullable=True),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('title', sa.VARCHAR(), nullable=True),
    sa.Column('body', sa.VARCHAR(), nullable=True),
    sa.Column('is_highlight', sa.BOOLEAN(), nullable=True),
    sa.Column('create_at', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.course_id'], ),
    sa.ForeignKeyConstraint(['create_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('comment_from', sa.INTEGER(), nullable=True),
    sa.Column('comment_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.INTEGER(), nullable=True),
    sa.Column('create_at', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['comment_from'], ['threads.id'], ),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments_pictures',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('from_comment', sa.INTEGER(), nullable=True),
    sa.Column('data', sa.BLOB(), nullable=True),
    sa.ForeignKeyConstraint(['from_comment'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('threads_pictures',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('from_thread', sa.INTEGER(), nullable=True),
    sa.Column('data', sa.BLOB(), nullable=True),
    sa.Column('order', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['from_thread'], ['threads.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('courses',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('course_id', sa.VARCHAR(), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('student_id', sa.VARCHAR(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.student_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('subcomments',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('reply_of', sa.INTEGER(), nullable=True),
    sa.Column('reply_data', sa.VARCHAR(), nullable=True),
    sa.Column('posted_by', sa.INTEGER(), nullable=True),
    sa.Column('create_at', sa.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['posted_by'], ['students.student_id'], ),
    sa.ForeignKeyConstraint(['reply_of'], ['comments.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###