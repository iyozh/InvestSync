import asyncio

import httpx


class ExternalAPIService:

    async def make_request(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()


    async def make_multiply_requests(self, urls):
        responses = await asyncio.gather(*[self.make_request(url) for url in urls])
        return responses
