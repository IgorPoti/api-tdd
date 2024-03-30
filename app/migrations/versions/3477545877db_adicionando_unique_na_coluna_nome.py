"""adicionando unique na coluna nome

Revision ID: 3477545877db
Revises: 9e1b37f78d1c
Create Date: 2024-03-30 18:21:35.019930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3477545877db'
down_revision: Union[str, None] = '9e1b37f78d1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'usuarios', ['nome'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'usuarios', type_='unique')
    # ### end Alembic commands ###