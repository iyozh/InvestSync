from datetime import date
from pydantic import BaseModel

class TickerHistory(BaseModel):
    open: float | None
    close: float | None
    high: float | None
    volume:int | None
    low: float | None
    date: date | None

    class Config:
        orm_mode = True
