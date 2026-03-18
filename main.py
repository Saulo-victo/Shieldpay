from src.infrastructure.sqlalchemy_repository import SqlAlchemyWalletRepository
from src.web.api import session


registro = SqlAlchemyWalletRepository(session)

# bob = registro.get_by_customer_id()


registro.set_register_balance("743edc48-5578-4707-ba8b-a22844bb86ed", '500')
