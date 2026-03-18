from src.domain.value_objects import Cpf, Email
from src.domain.entities import Customer, Wallet, Transaction
from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
import uuid
from src.domain.exceptions import InvalidTransaction, WalletNotFoundException
from datetime import datetime
from decimal import Decimal


class RegisterCustomer:
    def __init__(self, repository: SqlAlchemyUnitOfWork):
        self.uow = repository

    def execute(self, name, email, cpf):
        with self.uow as uow:
            email = Email(email)
            cpf = Cpf(cpf)
            id = str(uuid.uuid4())

            customer = Customer(id, name, email, cpf)

            uow.customers.save(customer)

            wallet = Wallet(str(uuid.uuid4()), str(customer.id), balance=0)
            uow.wallets.save(wallet)

            return customer


class TransferMoney:
    def __init__(self, repository: SqlAlchemyUnitOfWork):
        self.uow = repository

    def execute(self, payer_id, payee_id, amount):
        with self.uow as uow:
            payer_wallet = uow.wallets.get_by_customer_id(payer_id)
            payee_wallet = uow.wallets.get_by_customer_id(payee_id)
            if not payer_wallet or not payee_wallet:
                raise WalletNotFoundException("Cliente não encontrado")

            payer_wallet.withdraw(Decimal(amount))

            payer_wallet.balance = payer_wallet.balance - Decimal(amount)
            uow.wallets.change_register_balance(payer_wallet)

            payee_wallet.balance = payee_wallet.balance + Decimal(amount)
            uow.wallets.change_register_balance(payee_wallet)

            transaction = Transaction(str(uuid.uuid4()), str(
                payer_id), str(payee_id), amount, datetime.now())
            uow.transaction.save(transaction)
            return transaction
