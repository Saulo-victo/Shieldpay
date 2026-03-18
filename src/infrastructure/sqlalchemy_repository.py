from sqlalchemy.orm import Session
from src.domain.entities import Customer, Wallet, Transaction
from src.domain.repositories import ICustomerRepository, IWalletRepository, ITransactionRepository
from src.infrastructure.models import CustomerModel, WalletModel, TransactionModel
from decimal import Decimal


class SqlAlchemyCustomerRepository(ICustomerRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save(self, customer: Customer) -> None:
        db_customer = CustomerModel(
            id=str(customer.id),
            name=customer.name,
            email=customer.email.value,
            cpf=customer.cpf.value
        )
        self.session.add(db_customer)
        self.session.commit()


class SqlAlchemyWalletRepository(IWalletRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save(self, wallet: Wallet) -> None:
        db_wallet = WalletModel(
            id=str(wallet.id),
            id_customer=str(wallet.customer_id),
            balance=(wallet.balance)
        )
        self.session.add(db_wallet)
        self.session.commit()

    def get_by_customer_id(self, customer_id):
        model_wallet = self.session.query(
            WalletModel).filter_by(id_customer=customer_id).with_for_update().first()

        customer_wallet = Wallet(
            model_wallet.id, model_wallet.id_customer, Decimal(model_wallet.balance))

        return customer_wallet

    def change_register_balance(self, wallet) -> None:
        model_wallet = self.session.query(
            WalletModel).filter_by(id=wallet.id).with_for_update().first()
        model_wallet.balance = str(wallet.balance)
        self.session.commit()

    def set_register_balance(self, customer_id, new_balance) -> None:
        model_wallet = self.session.query(
            WalletModel).filter_by(id_customer=customer_id).with_for_update().first()
        model_wallet.balance = new_balance
        self.session.commit() #Esse método foi criado apenas para setar um depósito inicial, alterando o registro do balance. (EXCLUIR POSTERIORMENTE)


class SqlAlchemyTransactionRepository(ITransactionRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def save(self, transaction: Transaction) -> None:
        db_transaction = TransactionModel(
            id=str(transaction.id),
            id_payer=str(transaction.payer_id),
            id_payee=str(transaction.payee_id),
            amount=transaction.amount,
            created_at=transaction.created_at
        )
        self.session.add(db_transaction)
        self.session.commit()
