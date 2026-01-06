from app.core.config import settings
from app.services.base_client import BaseServiceClient


class UserServiceClient(BaseServiceClient):
    def __init__(self):
        super().__init__(settings.USER_SERVICE_URL)
