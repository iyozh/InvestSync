import sqlalchemy as sa
from app.src.db.base_class import Base


class TickerHistory(Base):
    __tablename__ = 'ticker_history'

    id = sa.Column(sa.Integer, primary_key=True)
    ticker_id = sa.Column(sa.Integer, sa.ForeignKey('ticker.id', ondelete='CASCADE'), nullable=False)
    open = sa.Column('open', sa.DECIMAL, nullable=False)
    high = sa.Column('high', sa.DECIMAL, nullable=False)
    low = sa.Column('low', sa.DECIMAL, nullable=False)
    close = sa.Column('close', sa.DECIMAL, nullable=False)
    volume = sa.Column('volume', sa.Integer, nullable=False)
    date = sa.Column('date', sa.Date, nullable=True)

    def __init__(self, ticker_id: str, open: str, high: str, low: str, close: str, volume: str, date: str):
        self.ticker_id = ticker_id
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.date = date
