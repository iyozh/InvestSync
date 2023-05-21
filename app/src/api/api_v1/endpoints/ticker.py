from typing import List
from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from app.src.api import dependencies
from app.src.repos.ticker_repo import TickerRepo
from app.src.schemas.filters import TickerHistoryFilter
from app.src.schemas.ticker import Ticker
from app.src.schemas.ticker_history import TickerHistory
from app.src.schemas.ticker_intraday_history import TickerIntraDayHistory
from app.src.schemas.ticker_quote import TickerQuote
from app.src.models.ticker import Ticker as TickerModel
from app.src.services.ticker_service import TickerService
from fastapi_limiter.depends import RateLimiter


router = APIRouter()

@router.get('/top', response_model=List[List[TickerQuote]], dependencies=[Depends(RateLimiter(times=3, seconds=5))])
async def get_tickers(
    db: Session = Depends(dependencies.get_db)
):
    """
    Retrieve top tickers.
    """

    ticker_service = TickerService()
    top_quotes = await ticker_service.get_top_tickers(db)
    return top_quotes


@router.get("/", response_model=List[Ticker], dependencies=[Depends(RateLimiter(times=5, seconds=5))])
def get_tickers(
    db: Session = Depends(dependencies.get_db),
    offset: int = 0, limit: int | None = None
):
    """
    Retrieve tickers.
    """

    ticker_repo = TickerRepo()
    return ticker_repo.get_multi(db, offset=offset, limit=limit)


@router.get("/{symbol}", response_model=Ticker, dependencies=[Depends(RateLimiter(times=5, seconds=5))])
def get_ticker(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    Retrieve ticker.
    """

    return ticker


@router.get('/history/{symbol}', response_model=List[TickerHistory], dependencies=[Depends(RateLimiter(times=5, seconds=5))])
def get_ticker_history(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404),
    ticker_history_filter: TickerHistoryFilter = FilterDepends(TickerHistoryFilter)
):
    """
    Retrieve ticker history
    :param ticker: Ticker object
    :param ticker_history_filter: Ticker History Filter
    :return List[TickerHistory]
    """

    filtered_query = ticker_history_filter.filter(ticker.history)
    sorted_query = ticker_history_filter.sort(filtered_query)
    return sorted_query.all()


@router.get('/intraday-prices/{symbol}', response_model=List[TickerIntraDayHistory], dependencies=[Depends(RateLimiter(times=5, seconds=5))])
async def get_intraday_prices(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    :param ticker: Ticker object
    :return List[TickerIntraDayHistory]
    """

    ticker_service = TickerService()
    intraday_prices = await ticker_service.get_ticker_intraday_prices(ticker)
    return intraday_prices


@router.get('/quote/{symbol}', response_model=List[TickerQuote], dependencies=[Depends(RateLimiter(times=5, seconds=5))])
async def get_ticker_quote(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    :param ticker: Ticker object
    :return List[TickerIntraDayHistory]
    """

    ticker_service = TickerService()
    quote = await ticker_service.get_ticker_quote(ticker)
    return quote
