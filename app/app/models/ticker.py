import sqlalchemy as sa
from app.app.db.base_class import Base


class Ticker(Base):
    __tablename__ = 'ticker'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    symbol = sa.Column(sa.VARCHAR(length=10))