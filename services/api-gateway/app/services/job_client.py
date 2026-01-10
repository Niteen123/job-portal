from app.core.config import settings
from app.services.base_client import BaseServiceClient


class JobServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.JOB_SERVICE_URL)

    async def get_jobs(self):
        return await self._request("GET", "/jobs")
