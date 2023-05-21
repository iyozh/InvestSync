import logging
import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from app.src.admin.ticker_admin import TickerAdmin
from app.src.admin.ticker_overview import TickerOverviewAdmin
from app.src.api.api_v1.api import api_router
from logging.config import dictConfig
from app.src.core.logging_config import LogConfig
from app.src.core.config import settings
from app.src.db.session import engine
from app.src.middlewares import ProcessRequestTimeMiddleware
from sqladmin import Admin

dictConfig(LogConfig().dict())
logger = logging.getLogger('invest-sync')

app = FastAPI()
app.include_router(api_router)

admin = Admin(app, engine)


admin.add_view(TickerAdmin)
admin.add_view(TickerOverviewAdmin)

my_middleware = ProcessRequestTimeMiddleware()
app.add_middleware(BaseHTTPMiddleware, dispatch=my_middleware)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
