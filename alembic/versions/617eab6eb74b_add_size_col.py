"""add size col

Revision ID: 617eab6eb74b
Revises: 4f4b8b1b6cde
Create Date: 2024-05-16 19:48:35.782459

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '617eab6eb74b'
down_revision: Union[str, None] = '4f4b8b1b6cde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company_dataset', sa.Column('size', sa.String(), nullable=False))
    op.add_column('user_dataset', sa.Column('size', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_dataset', 'size')
    op.drop_column('company_dataset', 'size')
    # ### end Alembic commands ###