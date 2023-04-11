import logging
import uvicorn
from fastapi import FastAPI
from app.src.api.api_v1.api import api_router
from logging.config import dictConfig
from app.src.core.logging_config import LogConfig
from app.src.core.config import settings

dictConfig(LogConfig().dict())
logger = logging.getLogger('invest-sync')

app = FastAPI()
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
