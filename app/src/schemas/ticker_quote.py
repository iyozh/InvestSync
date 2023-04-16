from pydantic import BaseModel


class TickerQuote(BaseModel):
    symbol: str | None
    change: float | None
    changePercent: float | None
    currency: str | None
    peRatio: float | None
    iexRealtimePrice: float | None
    latestPrice: float | None
