"""reset

Revision ID: 5067f5ce2dd8
Revises: c65c6ebcb439
Create Date: 2024-09-14 23:43:34.345247

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5067f5ce2dd8'
down_revision: Union[str, None] = 'c65c6ebcb439'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
