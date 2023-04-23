import asyncio

import httpx
import requests


class ExternalAPIService:
    @staticmethod
    async def make_request(url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()


    async def make_multiply_requests(self, urls):
        responses = await asyncio.gather(*[self.make_request(url) for url in urls])
        return responses

    @staticmethod
    def make_sync_request(url):
        response = requests.get(url)
        return response.json()
