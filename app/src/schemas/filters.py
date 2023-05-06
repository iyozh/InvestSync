from typing import Optional, List
from fastapi_filter.contrib.sqlalchemy import Filter
from app.src.models.ticker_history import TickerHistory


class TickerHistoryFilter(Filter):
    date: Optional[str]
    date__lte: Optional[str]
    date__gte: Optional[str]
    order_by: List[str] = ['date']
    close: Optional[int]
    close__gte: Optional[int]
    open: Optional[int]
    open__gte: Optional[int]
    high: Optional[int]
    high__gte: Optional[int]
    low: Optional[int]
    low__gte: Optional[int]
    volume: Optional[int]
    volume__gte: Optional[int]


    class Constants(Filter.Constants):
        model = TickerHistory
