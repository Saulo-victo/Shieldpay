from src.domain.interfaces import INotificantioService
import httpx


class WebhookNotificationService(INotificantioService):
    def __init__(self, url: str):
        self.url = url

    def send(self, user_id: str, message: str) -> bool:
        try:
            response = httpx.post(
                self.url,
                json={"user_id": user_id, "message": message},
                timeout=5.0
            )
            return response.status_code == 200
        except Exception:
            return False
