from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.src.api import dependencies
from app.src.repos.ticker_repo import TickerRepo
from app.src.schemas.ticker import Ticker

router = APIRouter()

@router.get("/", response_model=List[Ticker])
def get_tickers(
    db: Session = Depends(dependencies.get_db),
    offset: int = 0, limit: int | None = None
):
    """
    Retrieve tickers.
    """

    ticker_repo = TickerRepo()
    return ticker_repo.get_multi(db, offset=offset, limit=limit)


@router.get("/{symbol}", response_model=Ticker)
def get_ticker(
    symbol: str,
    db: Session = Depends(dependencies.get_db),
):
    """
    Retrieve ticker.
    """
    ticker_repo = TickerRepo()
    return ticker_repo.get_by_symbol(db, symbol)
