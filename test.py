import httpx
import asyncio

async def test():
    async with httpx.AsyncClient(timeout=10.0) as client: 
        responses = await asyncio.gather(
            client.get("http://localhost:8000/test"),
            client.get("http://localhost:8000/test"),
            client.get("http://localhost:8000/test")
        )
        for response in responses:
            print(response.json())

asyncio.run(test())
