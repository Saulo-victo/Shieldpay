from dataclasses import dataclass
from .value_objects import Cpf, Email, Money
from decimal import Decimal
import datetime
from src.domain.exceptions import InvalidTransaction


@dataclass
class Customer:
    id: str
    name: str
    email: Email
    cpf: Cpf


@dataclass
class Wallet:
    id: str
    customer_id: str
    balance: Money

    def withdraw(self, amount):
        if self.balance < amount:
            raise InvalidTransaction("Saldo insuficiente")


@dataclass
class Transaction:
    id: str
    payer_id: str
    payee_id: str
    amount: Money
    created_at: datetime
