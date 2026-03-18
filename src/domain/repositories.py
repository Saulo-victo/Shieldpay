from ..domain.entities import Customer, Wallet, Transaction
from abc import ABC, abstractmethod


class ICustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        pass


class IWalletRepository(ABC):
    @abstractmethod
    def save(self, wallet: Wallet) -> None:
        pass


class ITransactionRepository(ABC):
    @abstractmethod
    def save(self, transaction: Transaction) -> None:
        pass
