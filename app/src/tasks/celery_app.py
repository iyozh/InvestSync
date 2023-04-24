import json
from datetime import timedelta

from celery import Celery
from app.src.cache.redis_cache import redis_client
from app.src.core.config import settings
from app.src.core.constants import (INTRADAY_PRICES_API_URL, QUOTE_API_URL, QUOTE_EXPIRATION_TIME,
    INTRADAY_PRICES_EXPIRATION_TIME, HISTORY_PRICES_UPDATE_API_URL)
from app.src.db.session import SessionLocal
from app.src.models.ticker_history import TickerHistory
from app.src.repos.ticker_repo import TickerRepo
from app.src.services.external_api_service import ExternalAPIService
from app.src.main import logger
from app.src.services.redis_service import RedisService

app = Celery('invest-sync', broker=settings.CELERY_BROKER_URL)

app.conf.beat_schedule = {
    'refresh-quote-cache': {
        'task': 'app.src.tasks.celery_app.refresh_quote_cache',
        'schedule': 30.0
    },
    'refresh-intraday-prices-cache': {
        'task': 'app.src.tasks.celery_app.refresh_intraday_prices_cache',
        'schedule': 30.0
    },
    'refresh-historical-data': {
        'task': 'app.src.tasks.celery_app.refresh_historical_data',
        'schedule': 30.0
    },
}

@app.task
def refresh_intraday_prices_cache():
    db = SessionLocal()

    ticker_repo = TickerRepo()
    redis_service = RedisService()
    external_api_service = ExternalAPIService()

    tickers = ticker_repo.get_multi(db)

    for ticker in tickers:
        response = external_api_service.make_sync_request(
            INTRADAY_PRICES_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )

        logger.info(f"Intraday prices info received: {ticker.symbol}")
        redis_service.set_key(f"{ticker.symbol}:intraday-prices", response, INTRADAY_PRICES_EXPIRATION_TIME)

@app.task
def refresh_quote_cache():
    db = SessionLocal()

    ticker_repo = TickerRepo()
    external_api_service = ExternalAPIService()
    redis_service = RedisService()

    tickers = ticker_repo.get_multi(db)

    for ticker in tickers:
        response = external_api_service.make_sync_request(
            QUOTE_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )
        logger.info(f"Quote info received: {ticker.symbol} | {response}")
        redis_service.set_key(f"{ticker.symbol}:quote", response, QUOTE_EXPIRATION_TIME)


@app.task
def refresh_historical_data():
    db = SessionLocal()

    ticker_repo = TickerRepo()
    tickers = ticker_repo.get_multi(db)

    external_api_service = ExternalAPIService()


    ticker_history_prices = []
    for ticker in tickers:
        last_history_snapshot = ticker.history.order_by(TickerHistory.date.desc()).first()
        if not last_history_snapshot:
            continue
        history_from_date = last_history_snapshot.date + timedelta(days=1)

        ticker_history = external_api_service.make_sync_request(
            HISTORY_PRICES_UPDATE_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY,
                                                 date=history_from_date)
        )

        logger.info(f"Received {ticker.symbol} historical prices")

        if ticker_history:
            for fact in ticker_history:
                ticker_history_price = TickerHistory(ticker_id=ticker.id,
                                                     date=fact.get('priceDate'),
                                                     open=fact.get('open'),
                                                     close=fact.get('close'),
                                                     volume=fact.get('volume'),
                                                     low=fact.get('low'),
                                                     high=fact.get('high'))
                ticker_history_prices.append(ticker_history_price)

    db.bulk_save_objects(ticker_history_prices)
    db.commit()
