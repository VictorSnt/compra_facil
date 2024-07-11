from typing import List
from fastapi import APIRouter
from fastapi.params import Depends, Query

from src.factory.product_service_factory import ProductServiceFactory
from src.schemas.product_schema import GetProduct
from src.services.produto_service import ProductService



class ProductController:
    
    router = APIRouter(prefix='/products')
    
    @router.get('/', response_model=List[GetProduct])
    def get_produtos(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_Service
        ),
        only_active: bool = Query(True),
        familia_filter: List[str] = Query(None),
        grupo_filter: List[str] = Query(None)
        ):
        
        return service.find_all(only_active, familia_filter, grupo_filter)
    
    @router.get('/supplier_products', response_model=List[GetProduct])
    def get_supplier_products(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_Service
        ),
        fornecedor_ids: List[str] = Query() 
        ):
        
        return service.find_all_suppliers_products(fornecedor_ids)
    
    @router.get('/current_stock', response_model=List[GetProduct])
    def get_current_stock(
        service: ProductService = Depends(
            ProductServiceFactory.build_default_Service
        ),
        product_ids: List[str] = Query() 
        ):

        return service.find_products_with_current_stock(product_ids)
        
    
    @classmethod
    def get_router(cls):
        return cls.router
