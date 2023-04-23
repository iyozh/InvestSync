import json
from celery import Celery
from app.src.cache.redis_cache import redis_client
from app.src.core.config import settings
from app.src.core.constants import (INTRADAY_PRICES_API_URL, QUOTE_API_URL, QUOTE_EXPIRATION_TIME,
    INTRADAY_PRICES_EXPIRATION_TIME)
from app.src.db.session import SessionLocal
from app.src.repos.ticker_repo import TickerRepo
from app.src.services.external_api_service import ExternalAPIService
from app.src.main import logger

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
}

@app.task
def refresh_intraday_prices_cache():
    db = SessionLocal()

    ticker_repo = TickerRepo()
    tickers = ticker_repo.get_multi(db)

    external_api_service = ExternalAPIService()

    for ticker in tickers:
        response = external_api_service.make_sync_request(
            INTRADAY_PRICES_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )

        logger.info(f"Intraday prices info received: {ticker.symbol}")

        redis_client.set(f"{ticker.symbol}:intraday-prices",
                         json.dumps(response),
                         ex=INTRADAY_PRICES_EXPIRATION_TIME)
@app.task
def refresh_quote_cache():
    db = SessionLocal()

    ticker_repo = TickerRepo()
    tickers = ticker_repo.get_multi(db)

    external_api_service = ExternalAPIService()

    for ticker in tickers:
        response = external_api_service.make_sync_request(
            QUOTE_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
        )
        logger.info(f"Quote info received: {ticker.symbol} | {response}")
        redis_client.set(f"{ticker.symbol}:quote",
                         json.dumps(response),
                         ex=QUOTE_EXPIRATION_TIME)
