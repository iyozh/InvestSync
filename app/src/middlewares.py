import logging
import time
from fastapi import Request

logger = logging.getLogger('invest-sync')

class ProcessRequestTimeMiddleware:

    async def __call__(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request processed: {round(process_time, 2)} seconds")
        return response
