from app.src.schemas.ticker_history import TickerHistory


class TickerIntraDayHistory(TickerHistory):
    minute: str | None
