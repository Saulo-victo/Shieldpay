from dataclasses import dataclass
from src.domain.exceptions import InvalidEmailException, InvalidCpfException, InvalidValueMoney
from decimal import Decimal


@dataclass(frozen=True)
class Cpf:
    value: str

    def __post_init__(self):
        if not self.value.isdigit() or len(self.value) != 11:
            raise InvalidCpfException('Cpf inválido')


@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self):
        if '@' not in self.value:
            raise InvalidEmailException('Email Inválido')


@dataclass(frozen=True)
class Money:
    value: Decimal

    def __pos_init__(self):
        if self.value < 0:
            raise InvalidValueMoney('Saldo inválido')
