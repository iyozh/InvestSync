"""empty message

Revision ID: c48c2f14e1d3
Revises: 9f8268d363ee
Create Date: 2023-04-07 20:50:45.680314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c48c2f14e1d3'
down_revision = '9f8268d363ee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('ticker_history',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('ticker_id', sa.Integer, sa.ForeignKey('ticker.id', ondelete='CASCADE'),
                              nullable=False),
                    sa.Column('open', sa.DECIMAL, nullable=False),
                    sa.Column('high', sa.DECIMAL, nullable=False),
                    sa.Column('low', sa.DECIMAL, nullable=False),
                    sa.Column('close', sa.DECIMAL, nullable=False),
                    sa.Column('volume', sa.Integer, nullable=False),
                    sa.Column('date', sa.Date, nullable=True))


def downgrade() -> None:
    pass
