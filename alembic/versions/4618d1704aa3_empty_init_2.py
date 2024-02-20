"""Empty Init 2

Revision ID: 4618d1704aa3
Revises: 1968bd4a68c4
Create Date: 2024-02-20 12:55:56.417803

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4618d1704aa3'
down_revision: Union[str, None] = '1968bd4a68c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
