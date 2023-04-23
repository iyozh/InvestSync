import json
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.src.api import dependencies
from app.src.cache.redis_cache import redis_client
from app.src.core.config import settings
from app.src.core.constants import (INTRADAY_PRICES_API_URL, QUOTE_API_URL, QUOTE_EXPIRATION_TIME,
    INTRADAY_PRICES_EXPIRATION_TIME)
from app.src.repos.ticker_history_repo import TickerHistoryRepo
from app.src.repos.ticker_repo import TickerRepo
from app.src.schemas.ticker import Ticker
from app.src.schemas.ticker_history import TickerHistory
from app.src.schemas.ticker_intraday_history import TickerIntraDayHistory
from app.src.schemas.ticker_quote import TickerQuote
from app.src.services.external_api_service import ExternalAPIService
from app.src.models.ticker import Ticker as TickerModel

router = APIRouter()

@router.get('/top', response_model=List[List[TickerQuote]])
async def get_tickers(
    db: Session = Depends(dependencies.get_db)
):
    """
    Retrieve top tickers.
    """

    ticker_repo = TickerHistoryRepo()
    external_api_service = ExternalAPIService()

    symbols = ticker_repo.get_top_tickers_by_percentage_change(db)
    urls = [QUOTE_API_URL.format(symbol=symbol, api_key=settings.IEXCLOUD_API_KEY) for symbol in symbols]
    responses = await external_api_service.make_multiply_requests(urls)
    return responses


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
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    Retrieve ticker.
    """

    return ticker


@router.get('/history/{symbol}', response_model=List[TickerHistory])
def get_ticker_history(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    Retrieve ticker history
    :param ticker: Ticker object
    :return List[TickerHistory]
    """

    return ticker.history.all()


@router.get('/intraday-prices/{symbol}', response_model=List[TickerIntraDayHistory])
async def get_intraday_prices(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    :param ticker: Ticker object
    :return List[TickerIntraDayHistory]
    """

    cached_intraday_prices = redis_client.get(f"{ticker.symbol}:intraday-prices")
    intraday_prices = json.loads(cached_intraday_prices) if cached_intraday_prices else None

    if not intraday_prices:
        external_api_service = ExternalAPIService()
        intraday_prices = await external_api_service.make_request(
            INTRADAY_PRICES_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )
        redis_client.set(f"{ticker.symbol}:intraday-prices",
                         json.dumps(intraday_prices),
                         ex=INTRADAY_PRICES_EXPIRATION_TIME)

    return intraday_prices


@router.get('/quote/{symbol}', response_model=List[TickerQuote])
async def get_ticker_quote(
    ticker: TickerModel = Depends(dependencies.get_ticker_or_raise_404)
):
    """
    :param ticker: Ticker object
    :return List[TickerIntraDayHistory]
    """

    cached_quote = redis_client.get(f"{ticker.symbol}:quote")
    quote = json.loads(cached_quote) if cached_quote else None

    if not quote:
        external_api_service = ExternalAPIService()
        quote = await external_api_service.make_request(
            QUOTE_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )
        redis_client.set(f"{ticker.symbol}:quote",
                         json.dumps(quote),
                         ex=QUOTE_EXPIRATION_TIME)

    return quote
