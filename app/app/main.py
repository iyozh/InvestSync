import uvicorn
from fastapi import FastAPI
from app.app.api.api_v1.api import api_router
from app.app.core.config import settings

app = FastAPI()
app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)
