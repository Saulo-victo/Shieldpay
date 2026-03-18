from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.infrastructure.database import Base
from sqlalchemy import ForeignKey


class CustomerModel(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    cpf: Mapped[str] = mapped_column(unique=True)
    wallet = relationship(
        "WalletModel", back_populates="customer", uselist=False)

    customer_payer = relationship(
        "TransactionModel", foreign_keys="[TransactionModel.id_payer]", back_populates="payer")

    customer_payee = relationship(
        "TransactionModel", foreign_keys="[TransactionModel.id_payee]", back_populates="payee")


class WalletModel(Base):
    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(primary_key=True)
    id_customer: Mapped[str] = mapped_column(ForeignKey("customers.id"))
    balance: Mapped[str] = mapped_column(default=0.0)
    customer = relationship("CustomerModel", back_populates="wallet")


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True)
    id_payer: Mapped[str] = mapped_column(ForeignKey('customers.id'))
    id_payee: Mapped[str] = mapped_column(ForeignKey('customers.id'))
    amount: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)
    payer = relationship("CustomerModel", foreign_keys=[
                         id_payer], back_populates="customer_payer")
    payee = relationship("CustomerModel", foreign_keys=[
                         id_payee], back_populates="customer_payee")
