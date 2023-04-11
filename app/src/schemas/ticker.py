from pydantic import BaseModel

from app.src.schemas.ticker_overview import TickerOverview


class Ticker(BaseModel):
    symbol: str
    overview: TickerOverview

    class Config:
        orm_mode = True
