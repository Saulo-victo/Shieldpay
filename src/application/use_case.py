from src.domain.value_objects import Cpf, Email
from src.domain.entities import Customer, Wallet, Transaction
from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
import uuid
from src.domain.exceptions import InvalidTransaction, WalletNotFoundException
from datetime import datetime
from decimal import Decimal
from src.infrastructure.services.notification_service import WebhookNotificationService
from src.infrastructure.services.authorizer_service import ExternalAuthorizerService


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
    def __init__(self, repository: SqlAlchemyUnitOfWork, notification_service: WebhookNotificationService, authorizer_service: ExternalAuthorizerService):
        self.uow = repository
        self.notification_service = notification_service
        self.authorizer_service = authorizer_service

    def execute(self, payer_id, payee_id, amount):
        if not self.authorizer_service.is_authorized(payer_id, amount):
            raise Exception("Transação não autorizada pelo serviço externo.")

        with self.uow as uow:
            payer_wallet = uow.wallets.get_by_customer_id(payer_id)
            payee_wallet = uow.wallets.get_by_customer_id(payee_id)
            if not payer_wallet or not payee_wallet:
                raise WalletNotFoundException("Cliente não encontrado")

            payer_wallet.balance = payer_wallet.balance - Decimal(amount)
            uow.wallets.change_register_balance(payer_wallet)

            payee_wallet.balance = payee_wallet.balance + Decimal(amount)
            uow.wallets.change_register_balance(payee_wallet)

            payer_wallet.withdraw(Decimal(amount))
            if not self.notification_service.send(payee_wallet.customer_id, f"Recebido: R$ {amount}"):
                raise Exception(
                    "Erro de notificação: Transferência cancelada por segurança.")

            transaction = Transaction(str(uuid.uuid4()), str(
                payer_id), str(payee_id), amount, datetime.now())
            uow.transaction.save(transaction)
            return transaction
