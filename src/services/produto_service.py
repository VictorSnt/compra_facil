from typing import List
from fastapi import APIRouter

from src.exceptions.err import NotFoundException
from src.repository.produto_repository import ProdutoRepository
from src.schemas.produto_schema import GetProduto

router = APIRouter()


class ProdutoService:
    
    def __init__(self, repository: ProdutoRepository) -> None:
        self.repo = repository
    
    def find_all(self, only_active: bool, familia_filter: List[str]|None, grupo_filter: List[str]|None):
        
        response = self.repo.find_all(only_active, familia_filter, grupo_filter)
        
        if not response:
            raise NotFoundException
        print('serc')
        return [
            GetProduto(
                iddetalhe=produto.iddetalhe, 
                dsdetalhe=produto.dsdetalhe
            ) for produto in response
        ]

    def find_all_suppliers_products(self, fornecedor_ids):
        
        response = self.repo.find_products_by_suppliers(fornecedor_ids)
        
        if not response:
            raise NotFoundException
        
        return [
            GetProduto(iddetalhe=produto.iddetalhe, dsdetalhe=produto.dsdetalhe) 
            for produto in response
        ]
    
