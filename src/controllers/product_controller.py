#str
from typing import List
#ext
from fastapi import APIRouter, Query, Depends
#app
from src.factory.product_service_factory import ProductServiceFactory
from src.schemas.product_schema import GetProduct, GetProductWithStock
from src.services.produto_service import ProductService


class ProductController:

    router = APIRouter(prefix='/products')

    @staticmethod
    @router.get('/', response_model=List[GetProduct])
    def get_produtos(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_service
        ),
        only_active: bool = Query(True),
        familia_filter: List[str] = Query(None),
        grupo_filter: List[str] = Query(None)
        ):

        return service.find_all(only_active, familia_filter, grupo_filter)

    @staticmethod
    @router.get('/supplier_products', response_model=List[GetProduct])
    def get_supplier_products(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_service
        ),
        fornecedor_ids: List[str] = Query()
        ):

        return service.find_all_suppliers_products(fornecedor_ids)

    @staticmethod
    @router.get('/current_stock', response_model=List[GetProductWithStock])
    def get_current_stock(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_service
        ),
        product_ids: List[str] = Query(None)
        ):

        return service.find_products_with_current_stock(product_ids)

    @classmethod
    def get_router(cls):
        return cls.router
