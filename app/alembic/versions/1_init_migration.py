"""empty message

Revision ID: 9f8268d363ee
Revises: 
Create Date: 2023-04-02 10:28:04.987985

"""
from alembic import op
import sqlalchemy as sa

from app.src.core.constants import DEFAULT_FIELD_PLACEHOLDER

# revision identifiers, used by Alembic.
revision = '9f8268d363ee'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('ticker',
                    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True, nullable=False),
                    sa.Column('symbol', sa.VARCHAR(length=10), unique=True, nullable=False))

    op.create_table('ticker_overview',
                    sa.Column('ticker_id', sa.Integer, sa.ForeignKey('ticker.id', ondelete='CASCADE'),
                              nullable=False, primary_key=True),
                    sa.Column('name', sa.VARCHAR(length=200), nullable=False),
                    sa.Column('description', sa.VARCHAR(length=1000), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER),
                    sa.Column('country', sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER),
                    sa.Column('sector', sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER),
                    sa.Column('industry', sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER))
def downgrade() -> None:
    pass
