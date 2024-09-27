"""empty message

Revision ID: d9f34f86269c
Revises: 90cf6e3e02cd, e5f20708e6eb
Create Date: 2024-09-26 22:26:51.030671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9f34f86269c'
down_revision: Union[str, None] = ('90cf6e3e02cd', 'e5f20708e6eb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
