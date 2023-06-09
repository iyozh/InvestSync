from fastapi import APIRouter

from app.src.api.api_v1.endpoints import ticker

api_router = APIRouter()

api_router.include_router(ticker.router, prefix='/tickers')
