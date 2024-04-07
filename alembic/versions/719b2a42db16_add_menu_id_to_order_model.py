"""Add menu.id to Order model

Revision ID: 719b2a42db16
Revises: cb050ed8f5cf
Create Date: 2024-04-06 20:00:20.933651

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '719b2a42db16'
down_revision: Union[str, None] = 'cb050ed8f5cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('menu_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'order', 'menu', ['menu_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'menu_id')
    # ### end Alembic commands ###
