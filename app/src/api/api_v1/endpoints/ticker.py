from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.src.api import dependencies
from app.src.core.config import settings
from app.src.core.constants import INTRADAY_PRICES_API_URL, QUOTE_API_URL
from app.src.repos.ticker_history_repo import TickerHistoryRepo
from app.src.repos.ticker_repo import TickerRepo
from app.src.schemas.ticker import Ticker
from app.src.schemas.ticker_history import TickerHistory
from app.src.schemas.ticker_intraday_history import TickerIntraDayHistory
from app.src.services.external_api_service import ExternalAPIService

router = APIRouter()

@router.get('/top',)
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
    symbol: str,
    db: Session = Depends(dependencies.get_db),
):
    """
    Retrieve ticker.
    """
    ticker_repo = TickerRepo()
    ticker = ticker_repo.get_by_symbol(db, symbol)

    if not ticker:
        raise HTTPException(
            status_code=400, detail="Ticker doesn't exist"
        )

    return ticker


@router.get('/history/{symbol}', response_model=List[TickerHistory])
def get_ticker_history(
        symbol:str,
        db: Session = Depends(dependencies.get_db)
):
    """
    Retrieve ticker history
    :param db: dependency
    :param symbol: symbol name
    :return List[TickerHistory]
    """
    ticker_repo = TickerRepo()
    ticker = ticker_repo.get_by_symbol(db, symbol)

    if not ticker:
        raise HTTPException(
            status_code=400, detail="Ticker doesn't exist"
        )

    return ticker.history.all()


@router.get('/intraday-prices/{symbol}', response_model=List[TickerIntraDayHistory])
async def get_intraday_prices(
        symbol: str,
):
    """
    :param symbol: symbol name
    :return List[TickerIntraDayHistory]
    """

    external_api_service = ExternalAPIService()
    response = await external_api_service.make_request(
        INTRADAY_PRICES_API_URL.format(symbol=symbol, api_key=settings.IEXCLOUD_API_KEY)
    )
    return response


@router.get('/quote/{symbol}')
async def get_ticker_quote(
        symbol: str,
):
    """
    :param symbol: symbol name
    :return List[TickerIntraDayHistory]
    """

    external_api_service = ExternalAPIService()
    response = await external_api_service.make_request(
        QUOTE_API_URL.format(symbol=symbol, api_key=settings.IEXCLOUD_API_KEY)
    )
    return response
