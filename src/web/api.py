import os
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from http import HTTPStatus
from src.infrastructure.unit_of_work import SqlAlchemyUnitOfWork
from src.application.use_case import RegisterCustomer, TransferMoney
from src.domain.exceptions import InvalidCpfException, InvalidEmailException, InvalidCreateUser, InvalidTransaction
from src.infrastructure.database import engine, Base
from src.infrastructure.database import SessionLocal
from datetime import datetime, timezone
from decimal import Decimal
from dotenv import load_dotenv
from src.infrastructure.services.notification_service import WebhookNotificationService
from src.infrastructure.services.authorizer_service import ExternalAuthorizerService
from sqlalchemy.exc import IntegrityError

load_dotenv()

NOTIFICATION_URL = os.getenv('NOTIFICATION_URL')
notification_service = WebhookNotificationService(NOTIFICATION_URL)

AUTHORIZER_URL = os.getenv('AUTHORIZER_URL')
authorizer_service = ExternalAuthorizerService(AUTHORIZER_URL)

Base.metadata.create_all(bind=engine)

session = SessionLocal()


class CustomerResponse(BaseModel):
    id: str
    name: str
    email: str
    cpf: str


class CustomerRequest(BaseModel):
    name: str
    email: str
    cpf: str


class Message(BaseModel):
    message: str


class TranserRequest(BaseModel):
    payer_id: str
    payee_id: str
    amount: str


class TransferResponse(BaseModel):
    id: str
    payer_id: str
    payee_id: str
    amount: str
    create_at: str


app = FastAPI()

memory_unit_of_work = SqlAlchemyUnitOfWork()


def get_register_use_case():
    register = RegisterCustomer(memory_unit_of_work)
    return register


@app.post("/customers/", response_model=CustomerResponse, status_code=HTTPStatus.CREATED)
def register_customer(request: CustomerRequest, use_case=Depends(get_register_use_case)):
    try:
        customer = use_case.execute(**request.model_dump())
        return {
            "id": str(customer.id),
            "name": customer.name,
            "email": str(customer.email.value),
            "cpf": str(customer.cpf.value)
        }
    except IntegrityError:
        raise InvalidCreateUser('O cliente já existe')


@app.exception_handler(InvalidCpfException)
def cpf_exeption_handler(request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(InvalidEmailException)
def email_exeption_handler(request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


@app.exception_handler(InvalidCreateUser)
def user_exeption_handler(request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})


def get_transfer_money_use_case():
    transfer = TransferMoney(
        memory_unit_of_work, notification_service, authorizer_service)
    return transfer


@app.post("/transfer/", response_model=TransferResponse, status_code=HTTPStatus.CREATED)
def transfer_money(request: TranserRequest, use_case=Depends(get_transfer_money_use_case)):
    transaction = use_case.execute(**request.model_dump())
    return {
        "id": str(transaction.id),
        "payer_id": str(transaction.payer_id),
        "payee_id": str(transaction.payee_id),
        "amount": str(transaction.amount),
        "create_at": str(transaction.created_at)
    }


@app.exception_handler(InvalidTransaction)
def transaction_insufficient_balance(request, exc):
    return JSONResponse(status_code=HTTPStatus.BAD_REQUEST, content={'message': str(exc)})
