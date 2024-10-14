"""create users table

Revision ID: 092eddacf318
Revises: a2bcfed6ffb7
Create Date: 2024-10-13 23:18:55.362255

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "092eddacf318"
down_revision: Union[str, None] = "a2bcfed6ffb7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("username", name=op.f("uq_user_username")),
    )


def downgrade() -> None:
    op.drop_table("user")
