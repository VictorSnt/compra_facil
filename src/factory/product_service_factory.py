from fastapi.params import Depends
from sqlalchemy.orm import Session

from src.database.db_session_maker import Session_Maker
from src.model.product import Product
from src.model.product_info import ProductInfo
from src.repository.product_repository import ProductRepository
from src.services.produto_service import ProductService


class ProductServiceFactory:
    
    @classmethod
    def build_default_Service(
        cls, session: Session = Depends(Session_Maker.create_session)):
        
        repo = ProductRepository(session, Product, ProductInfo)
        return ProductService(repo)
