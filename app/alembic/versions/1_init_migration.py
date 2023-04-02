"""empty message

Revision ID: 9f8268d363ee
Revises: 
Create Date: 2023-04-02 10:28:04.987985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f8268d363ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('ticker',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column('symbol', sa.VARCHAR(length=10), unique=True))


def downgrade() -> None:
    pass
