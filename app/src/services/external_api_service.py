import asyncio
import httpx
import requests
from fastapi import HTTPException
from starlette import status


class ExternalAPIService:
    @staticmethod
    async def make_request(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == status.HTTP_200_OK:
                return response.json()
            else:
                raise HTTPException(status_code=500, detail="Service temporary unavailable.")

    async def make_multiply_requests(self, urls):
        responses = await asyncio.gather(*[self.make_request(url) for url in urls])
        return responses

    @staticmethod
    def make_sync_request(url):
        response = requests.get(url)
        if response.status_code == status.HTTP_200_OK:
            return response.json()
        else:
            raise HTTPException(status_code=500, detail="Service temporary unavailable.")
