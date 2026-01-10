from app.core.config import settings
from app.services.base_client import BaseServiceClient


class AuthServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.AUTH_SERVICE_URL)

    async def login(self, payload: dict):
        return await self._request(
            method="POST",
            path="/login",
            json=payload
        )
