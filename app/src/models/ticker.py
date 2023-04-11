import sqlalchemy as sa
from sqlalchemy.orm import relationship
from app.src.db.base_class import Base
from app.src.models.ticker_history import TickerHistory
from app.src.models.ticker_overview import TickerOverview


class Ticker(Base):
    __tablename__ = 'ticker'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    symbol = sa.Column(sa.VARCHAR(length=10))

    overview = relationship(TickerOverview, uselist=False)
    history = relationship(TickerHistory, lazy='dynamic')

    def __init__(self, symbol: str):
        self.symbol = symbol
