import sqlalchemy as sa
from app.src.core.constants import DEFAULT_FIELD_PLACEHOLDER
from app.src.db.base_class import Base


class TickerOverview(Base):
    __tablename__ = 'ticker_overview'

    ticker_id = sa.Column(sa.Integer, sa.ForeignKey('ticker.id', ondelete='CASCADE'),
                          primary_key=True, autoincrement=True)
    name = sa.Column(sa.VARCHAR(length=200), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER)
    description = sa.Column(sa.VARCHAR(length=5000), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER)
    country = sa.Column(sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER)
    sector = sa.Column(sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER)
    industry = sa.Column(sa.VARCHAR(length=100), nullable=False, default=DEFAULT_FIELD_PLACEHOLDER)

    def __init__(self, ticker_id: int, name: str, description: str, country: str, sector: str, industry: str):
        self.ticker_id = ticker_id
        self.name = name
        self.description = description
        self.country = country
        self.sector = sector
        self.industry = industry
