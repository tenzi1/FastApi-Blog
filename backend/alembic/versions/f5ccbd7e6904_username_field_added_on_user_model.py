"""username field added on user model

Revision ID: f5ccbd7e6904
Revises: 08b813d920a4
Create Date: 2024-03-22 09:07:08.654816

"""
from typing import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "f5ccbd7e6904"
down_revision: Union[str, None] = "08b813d920a4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_group_id", table_name="group")
    op.drop_table("group")
    op.add_column("user", sa.Column("username", sa.String(), nullable=True))
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_column("user", "username")
    op.create_table(
        "group",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="group_pkey"),
        sa.UniqueConstraint("name", name="group_name_key"),
    )
    op.create_index("ix_group_id", "group", ["id"], unique=False)
    # ### end Alembic commands ###
