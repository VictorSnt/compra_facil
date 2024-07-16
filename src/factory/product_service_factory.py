#ext
from fastapi import Depends
from sqlalchemy.orm import Session
#app
from src.database.db_session_maker import SessionMaker
from src.model.product import Product
from src.model.product_info import ProductInfo
from src.repository.product_repository import ProductRepository
from src.services.produto_service import ProductService


class ProductServiceFactory:

    @classmethod
    def build_default_service(
        cls, session: Session = Depends(SessionMaker.alterdata_session)):

        repo = ProductRepository(session, Product, ProductInfo)
        return ProductService(repo)
