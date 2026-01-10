import httpx
from fastapi import Request

class BaseServiceClient:
    def __init__(self, base_url: str, timeout: float = 3.0):
        self.base_url = base_url
        self.timeout = timeout

    async def _request(self, method: str, path: str, request: Request = None, **kwargs):
        headers = kwargs.pop("headers", {})

        if request:
            headers["X-Request-ID"] = request.state.request_id

        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                f"{self.base_url}{path}",
                headers=headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()
