"""create queries table

Revision ID: a2bcfed6ffb7
Revises: 
Create Date: 2024-10-13 23:18:03.460972

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a2bcfed6ffb7"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "query",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cadastre_number", sa.String(), nullable=False),
        sa.Column("latitude", sa.String(), nullable=False),
        sa.Column("longitude", sa.String(), nullable=False),
        sa.Column("result", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_query")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table("query")
