from sqlalchemy.orm import Session

from app.src.core.config import settings
from app.src.core.constants import (QUOTE_API_URL, QUOTE_EXPIRATION_TIME, INTRADAY_PRICES_API_URL,
    INTRADAY_PRICES_EXPIRATION_TIME)
from app.src.enums import RedisLabel
from app.src.models.ticker import Ticker
from app.src.repos.ticker_history_repo import TickerHistoryRepo
from app.src.repos.ticker_repo import TickerRepo
from app.src.services.base_service import BaseService
from app.src.services.external_api_service import ExternalAPIService
from app.src.services.redis_service import RedisService


class TickerService(BaseService):
    """Service layer for Ticker model to manage business logic."""

    def __init__(self, repo_class=TickerRepo):
        super().__init__(repo_class=repo_class)
        self.redis_service = RedisService()
        self.external_api_service = ExternalAPIService()

    async def get_ticker_quote(self, ticker: Ticker):
        key = f'{ticker.symbol}:{RedisLabel.quote.value}'
        quote = await self.redis_service.get_cached_value(key)

        if not quote:
            quote = await self.external_api_service.make_request(
                QUOTE_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
            )
            await self.redis_service.set_key(key, quote, QUOTE_EXPIRATION_TIME)

        return quote

    async def get_ticker_intraday_prices(self, ticker: Ticker):
        key = f'{ticker.symbol}:{RedisLabel.intraday_prices.value}'
        intraday_prices = await self.redis_service.get_cached_value(key)

        if not intraday_prices:
            quote = await self.external_api_service.make_request(
                INTRADAY_PRICES_API_URL.format(symbol=ticker.symbol, api_key=settings.IEXCLOUD_API_KEY)
            )
            await self.redis_service.set_key(key, quote, INTRADAY_PRICES_EXPIRATION_TIME)

        return intraday_prices

    @staticmethod
    async def get_top_tickers(db: Session):
        ticker_repo = TickerHistoryRepo()
        external_api_service = ExternalAPIService()

        symbols = ticker_repo.get_top_tickers_by_percentage_change(db)
        urls = [QUOTE_API_URL.format(symbol=symbol, api_key=settings.IEXCLOUD_API_KEY) for symbol in symbols]

        top_quotes = await external_api_service.make_multiply_requests(urls)
        return top_quotes
