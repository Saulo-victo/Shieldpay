from abc import ABC, abstractmethod
from decimal import Decimal


class INotificantioService(ABC):
    @abstractmethod
    def send(self, user_id: str, message: str) -> None:
        pass


class IAuthorizerService(ABC):
    @abstractmethod
    def is_authorized(self, payer_id: str, amount: Decimal) -> bool:
        pass
