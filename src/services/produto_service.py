from typing import List
from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.product_repository import ProductRepository
from src.schemas.product_schema import GetProduct

router = APIRouter()


class ProductService:
    
    def __init__(self, repository: ProductRepository) -> None:
        self.repo = repository
    
    def find_all(self, only_active: bool, familia_filter: List[str]|None, grupo_filter: List[str]|None):
        
        response = self.repo.find_all(only_active, familia_filter, grupo_filter)
        
        if not response:
            raise NotFoundException
        print('serc')
        return [
            GetProduct(
                iddetalhe=product.iddetalhe, 
                dsdetalhe=product.dsdetalhe
            ) for product in response
        ]

    def find_all_suppliers_products(self, fornecedor_ids):
        
        response = self.repo.find_products_by_suppliers(fornecedor_ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetProduct(iddetalhe=product.iddetalhe, dsdetalhe=product.dsdetalhe) 
            for product in response
        ]
    
    def find_products_with_current_stock(self, product_ids):
        
        response = self.repo.find_products_with_current_stock(product_ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetProduct(iddetalhe=product.iddetalhe, dsdetalhe=product.dsdetalhe) 
            for product in response
        ]