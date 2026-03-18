from src.infrastructure.database import SessionLocal
from src.infrastructure.sqlalchemy_repository import SqlAlchemyCustomerRepository, SqlAlchemyWalletRepository, SqlAlchemyTransactionRepository


class SqlAlchemyUnitOfWork:
    def __enter__(self):
        self.session = SessionLocal()
        self.customers = SqlAlchemyCustomerRepository(self.session)
        self.wallets = SqlAlchemyWalletRepository(self.session)
        self.transaction = SqlAlchemyTransactionRepository(self.session)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
