import httpx
from src.domain.interfaces import IAuthorizerService


class ExternalAuthorizerService(IAuthorizerService):
    def __init__(self, url):
        self.url = url

    def is_authorized(self, payer_id, amount):
        try:
            response = httpx.get(self.url, timeout=3.0)
            data = response.json()
            return response.status_code == 200 and data.get("data", {}).get("authorization") is True
        except Exception:
            return False
