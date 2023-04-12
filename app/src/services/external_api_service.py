import httpx


class ExternalAPIService:

    async def make_request(self, url):
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            return response.json()
